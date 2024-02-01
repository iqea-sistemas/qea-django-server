from rest_framework import serializers
from .models import IqeaUser, Projects



class IqeaUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = IqeaUser
        #fields=('id', 'user','name','last_name','email','phone','company','created','isAdmin')
        fields='__all__'


class ProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields='__all__'
