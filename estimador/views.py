from django.shortcuts import render
from rest_framework import viewsets, generics, status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializer import IqeaUserSerializer, UserSerializer,CotizacionSerializer
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


# @permission_classes([IsAuthenticated])
# class ProjectsView(viewsets.ModelViewSet):
#     serializer_class = CotizacionSerializer
#     queryset = Cotizacion.objects.all()



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
            cotizacion = serializer.save()
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
