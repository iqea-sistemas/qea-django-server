from rest_framework import serializers
from .models import IqeaUser, ProjectData, SystemCotizacion, SystemCotizacion,SystemCotizacion, Cotizacion, PrecioRefPoint, SystemType, SystemCategory
from django.contrib.auth.models import User



class IqeaUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = IqeaUser
        #fields=('id', 'user','name','last_name','email','phone','company','created','isAdmin')
        fields='__all__'

# Bases de cotizacion
class SystemTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemType
        fields = '__all__'

class SystemCategorySerializer(serializers.ModelSerializer):
    system_category = SystemTypeSerializer(many=True, read_only=True)

    class Meta:
        model = SystemCategory
        fields = '__all__'

# Projectos
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectData
        fields = '__all__'

class WaterSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemCotizacion
        fields = '__all__'

class WasteWaterSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemCotizacion
        fields = '__all__'

class ReusoSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemCotizacion
        fields = '__all__'

class CotizacionSerializer(serializers.ModelSerializer):
    project_data = ProjectSerializer()
    clean_water_system = WaterSystemSerializer(many=True)
    waste_water_system = WasteWaterSystemSerializer(many=True)
    reuso_water_system = ReusoSystemSerializer(many=True)

    class Meta:
        model = Cotizacion
        fields = '__all__'

    def create(self, validated_data):
        project_data = validated_data.pop('project_data')
        water_cotizacion_data = validated_data.pop('clean_water_system', [])
        waste_water_cotizacion_data = validated_data.pop('waste_water_system', [])
        reuso_cotizacion_data = validated_data.pop('reuso_water_system', [])

        # Crear una instancia de ProjectData
        project_data_instance = ProjectData.objects.create(**project_data)
        cotizacion = Cotizacion.objects.create(project_data=project_data_instance, **validated_data)

        water_intances = []
        for water_data in water_cotizacion_data:
            water_intance = SystemCotizacion.objects.create(**water_data)
            water_intances.append(water_intance)
        cotizacion.clean_water_system.set(water_intances)

        waste_water_instances = []
        for waste_water_data in waste_water_cotizacion_data:
            waste_water_instance = SystemCotizacion.objects.create(**waste_water_data)
            waste_water_instances.append(waste_water_instance)
        cotizacion.waste_water_system.set(waste_water_instances)

        reuso_instances = []
        for reuso_data in reuso_cotizacion_data:
            reuso_instance = SystemCotizacion.objects.create(**reuso_data)
            reuso_instances.append(reuso_instance)

        cotizacion.reuso_water_system.set(reuso_instances)

        return cotizacion

    def update(self, instance, validated_data):
        instance.project_data.name = validated_data.get('project_data', instance.project_data).get('name', instance.project_data.name)
        instance.project_data.location = validated_data.get('project_data', instance.project_data).get('location', instance.project_data.location)
        instance.project_data.date = validated_data.get('project_data', instance.project_data).get('date', instance.project_data.date)
        instance.project_data.save()

        # Actualizar clean_water_system
        clean_water_system_data = validated_data.get('clean_water_system')
        if clean_water_system_data:
            for data in clean_water_system_data:
                instance.clean_water_system.create(**data)

        # Actualizar waste_water_system
        waste_water_system_data = validated_data.get('waste_water_system')
        if waste_water_system_data:
            for data in waste_water_system_data:
                instance.waste_water_system.create(**data)

        # Actualizar reuso_water_system
        reuso_water_system_data = validated_data.get('reuso_water_system')
        if reuso_water_system_data:
            for data in reuso_water_system_data:
                instance.reuso_water_system.create(**data)

        return instance




#Registro de usuarios
class IqeaUserSerializer(serializers.ModelSerializer):
    cotizaciones = serializers.SerializerMethodField()

    class Meta:
        model = IqeaUser
        fields = ['id', 'username', 'name', 'last_name', 'email', 'phone', 'company', 'isAdmin', 'cotizaciones']

    def get_cotizaciones(self, obj):
        cotizaciones = Cotizacion.objects.filter(user=obj)
        serializer = CotizacionSerializer(cotizaciones, many=True)
        return serializer.data

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


class PrecioRefPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrecioRefPoint
        fields = '__all__'
