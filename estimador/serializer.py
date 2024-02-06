from rest_framework import serializers
from .models import IqeaUser, ProjectData, PriceValue, Cotizacion
from django.contrib.auth.models import User



class IqeaUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = IqeaUser
        #fields=('id', 'user','name','last_name','email','phone','company','created','isAdmin')
        fields='__all__'





# Projectos
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectData
        fields = '__all__'

class PriceValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceValue
        fields = '__all__'

class CotizacionSerializer(serializers.ModelSerializer):
    project_data = ProjectSerializer()
    water_cotizacion = PriceValueSerializer(many=True, read_only=True)
    waste_water_cotizacion = PriceValueSerializer(many=True, read_only=True)
    reuso_cotizacion = PriceValueSerializer(many=True, read_only=True)

    class Meta:
        model = Cotizacion
        fields = '__all__'





#Registro de usuarios
class IqeaUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = IqeaUser
        fields = ['username','name', 'last_name', 'email', 'phone', 'company', 'isAdmin']

class UserSerializer(serializers.ModelSerializer):
    iqea_user = IqeaUserSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'iqea_user']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        iqea_user_data = validated_data.pop('iqea_user')
        user = User.objects.create_user(**validated_data)
        IqeaUser.objects.create(user=user, **iqea_user_data)
        return user
