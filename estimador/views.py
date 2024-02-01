from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializer import IqeaUserSerializer, ProjectsSerializer
from .models import *


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

        return token

class MyTokenObteainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class IqeaUserView(viewsets.ModelViewSet):
    serializer_class = IqeaUserSerializer
    queryset = IqeaUser.objects.all()



class ProjectsView(viewsets.ModelViewSet):
    serializer_class = ProjectsSerializer
    queryset = Projects.objects.all()
