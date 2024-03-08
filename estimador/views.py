from django.shortcuts import render
import numpy as np
from rest_framework import viewsets, generics, status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializer import IqeaUserSerializer, UserSerializer,CotizacionSerializer, SystemCategorySerializer, PreciosReferenciaSerializer
from .models import *



#Registro de usuarios
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.permissions import AllowAny
# from .serializers import UserSerializer

class RegisterUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Usuario registrado exitosamente'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Create your views here.
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['name'] = user.first_name
        token['username'] = user.username
        token['email'] = user.email
        iqea_user = user.iqeauser if hasattr(user, 'iqeauser') else None
        # Add custom claims from IqeaUser model
        if iqea_user:
            token['company'] = iqea_user.company
            token['phone'] = iqea_user.phone
            token['isAdmin']=iqea_user.isAdmin
        return token

class MyTokenObteainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer



class IqeaUserView(viewsets.ModelViewSet):
    serializer_class = IqeaUserSerializer
    queryset = IqeaUser.objects.all()


@permission_classes([IsAuthenticated])
class adminProjectsView(viewsets.ModelViewSet):
    serializer_class = CotizacionSerializer
    queryset = Cotizacion.objects.all()



@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def ProjectsView(request, cotizacion_id=None):
    user = request.user
    iqea_user = IqeaUser.objects.get(user=user)

    if request.method == 'GET':
        # Manejar solicitud GET
        cotizaciones = Cotizacion.objects.filter(user=iqea_user)
        serializer = CotizacionSerializer(cotizaciones, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # Manejar solicitud POST
        serializer = CotizacionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['user'] = iqea_user
            # cotizacion = serializer.save()

            # Calcular precios para sistemas de tratamiento de agua
            for system_type, systems in serializer.validated_data.items():
                if system_type in ['clean_water_system', 'waste_water_system', 'reuso_water_system']:
                    for system in systems:
                        tipo_sistema = system['system_type']
                        flujo = system['flow']
                        resultado = calcular_precio(tipo_sistema, flujo)
                        precio = resultado['precio']
                        currency = resultado['currency']
                        system['price'] = precio
                        system['currency']=currency
            serializer.save()  # Guardamos los cambios en la cotización

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    elif request.method == 'PUT':
        # Manejar solicitud PUT para actualizar una cotización existente
        try:
            cotizacion = Cotizacion.objects.get(id=cotizacion_id, user=iqea_user)
        except Cotizacion.DoesNotExist:
            return Response({"error": "Cotizacion no encontrada"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CotizacionSerializer(cotizacion, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # Manejar solicitud DELETE para eliminar una cotización existente
        print('le delete',cotizacion_id)
        print(user)
        try:
            cotizacion = Cotizacion.objects.get(id=cotizacion_id, user=iqea_user)
        except Cotizacion.DoesNotExist:
            return Response({"error": "Cotizacion no encontrada"}, status=status.HTTP_404_NOT_FOUND)

        cotizacion.delete()
        response_data = {
            "details": "Cotizacion Eliminada",
            "ok": True,
            "status": status.HTTP_200_OK
        }
        return Response(response_data)
    return Response(status=status.HTTP_204_NO_CONTENT)



class PrecioEstimado(APIView):
    def get(self, request, tipo_sistema, f):
        # Obtener todos los PrecioRefPoint que pertenecen al tipo de sistema dado
        puntos_referencia = PrecioRefPoint.objects.filter(precios_referencia__system_type=tipo_sistema)

        # Crear listas para almacenar los valores de flujo y precioFinal
        flujo_list = []
        precio_final_list = []

        # Llenar las listas con los valores de flujo y precioFinal
        for punto in puntos_referencia:
            flujo_list.append(float(punto.flujo))
            precio_final_list.append(float(punto.precioFinal))

        # Convertir las listas a arrays numpy
        x = np.array(flujo_list)
        y = np.array(precio_final_list)

        # Calcular los coeficientes del polinomio de ajuste
        coef = np.polyfit(x, y, 2)

        # Calcular el nuevo valor 'y' para el valor 'f' dado
        nuevo_y = np.polyval(coef, float(f))

        # Retornar el nuevo valor 'y' en formato JSON
        return Response({'Precio': nuevo_y})


@permission_classes([IsAuthenticated])
class SystemCategoryList(generics.ListAPIView):
    queryset = SystemCategory.objects.all()
    serializer_class = SystemCategorySerializer


@permission_classes([IsAuthenticated])
class PreciosRefenciaList(generics.ListAPIView):
    queryset = PreciosReferencia.objects.prefetch_related('system_type')
    serializer_class = PreciosReferenciaSerializer



@permission_classes([IsAuthenticated])
class PreciosRefenciaDetail(generics.RetrieveAPIView):
    queryset = PreciosReferencia.objects.all()
    serializer_class = PreciosReferenciaSerializer


def calcular_precio(tipo_sistema, f):
  # Obtener todos los PrecioRefPoint que pertenecen al tipo de sistema dado
    puntos_referencia = PrecioRefPoint.objects.filter(precios_referencia__system_type=tipo_sistema)

    # Crear listas para almacenar los valores de flujo y precioFinal
    flujo_list = []
    precio_final_list = []
    currency_list = []

    # Llenar las listas con los valores de flujo y precioFinal
    for punto in puntos_referencia:
        flujo_list.append(float(punto.flujo))
        precio_final_list.append(float(punto.precioFinal))
        currency_list.append(punto.currency)

    # Convertir las listas a arrays numpy
    x = np.array(flujo_list)
    y = np.array(precio_final_list)

    # Calcular los coeficientes del polinomio de ajuste
    coef = np.polyfit(x, y, 2)

    # Calcular el nuevo valor 'y' para el valor 'f' dado
    nuevo_y = np.polyval(coef, float(f))
    nuevo_y = round(nuevo_y, 2)

    # Obtener el currency correspondiente al valor 'f' dado
    currency = currency_list[0]

    # Retornar el nuevo valor 'y' en formato JSON
    if nuevo_y:
      return {'precio': nuevo_y, 'currency': currency}
    return 0

