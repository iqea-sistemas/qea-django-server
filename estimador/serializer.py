from rest_framework import serializers
from .models import IqeaUser, ProjectData, WaterSystem, WasteWaterSystem,ReusoSystem, Cotizacion
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

class WaterSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterSystem
        fields = '__all__'

class WasteWaterSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteWaterSystem
        fields = '__all__'

class ReusoSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReusoSystem
        fields = '__all__'

class CotizacionSerializer(serializers.ModelSerializer):
    project_data = ProjectSerializer()
    water_cotizacion = WaterSystemSerializer(many=True)
    waste_water_cotizacion = WasteWaterSystemSerializer(many=True)
    reuso_cotizacion= ReusoSystemSerializer(many=True)

    class Meta:
        model = Cotizacion
        fields = '__all__'

    def create(self, validated_data):
        project_data = validated_data.pop('project_data')
        water_cotizacion_data = validated_data.pop('water_cotizacion', [])
        waste_water_cotizacion_data = validated_data.pop('waste_water_cotizacion', [])
        reuso_cotizacion_data = validated_data.pop('reuso_cotizacion', [])

        # Crear una instancia de ProjectData
        project_data_instance = ProjectData.objects.create(**project_data)
        cotizacion = Cotizacion.objects.create(project_data=project_data_instance,  **validated_data)

        water_intances=[]
        for water_data in water_cotizacion_data:
            water_intance=WaterSystem.objects.create(**water_data)
            water_intances.append(water_intance)
        cotizacion.water_cotizacion.set(water_intances)

        waste_water_instances=[]
        for waste_water_data in waste_water_cotizacion_data:
            waste_water_instance= WasteWaterSystem.objects.create(**waste_water_data)
            waste_water_instances.append(waste_water_instance)
        cotizacion.waste_water_cotizacion.set(waste_water_instances)


        reuso_instances = []
        for reuso_data in reuso_cotizacion_data:
            reuso_instance = ReusoSystem.objects.create(**reuso_data)
            reuso_instances.append(reuso_instance)

        cotizacion.reuso_cotizacion.set(reuso_instances)

        return cotizacion




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
