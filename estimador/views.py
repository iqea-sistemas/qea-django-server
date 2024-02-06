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


@permission_classes([IsAuthenticated])
class ProjectsView(viewsets.ModelViewSet):
    serializer_class = CotizacionSerializer
    queryset = Cotizacion.objects.all()
