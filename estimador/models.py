from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class IqeaUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100,null=True, blank=True )
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=100)
    company = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    isAdmin = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class ProjectData(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    date = models.DateField()

    def __str__(self):
        return self.name

class PriceValue(models.Model):
    system = models.CharField(max_length=255, blank=True, null=True)
    flow = models.FloatField(blank=True, null=True)
    unit = models.CharField(max_length=255, blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    currency = models.CharField(max_length=255, blank=True, null=True)
    cotizacion = models.ManyToManyField('Cotizacion', blank=True,  db_index=True )

    def __str__(self):
        # project_name = self.cotizacion.project_data.name if self.cotizacion and self.cotizacion.project_data else ""
        return f"{self.system}"

class Cotizacion(models.Model):
    user = models.ForeignKey(IqeaUser, on_delete=models.CASCADE, null=True, blank=True,  db_index=True )
    created = models.DateTimeField(auto_now_add=True)
    project_data = models.ForeignKey(ProjectData, on_delete=models.CASCADE, null=True, blank=True)
    water_cotizacion = models.ManyToManyField(PriceValue, related_name='water_cotizacion', blank=True)
    waste_water_cotizacion = models.ManyToManyField(PriceValue, related_name='waste_water_cotizacion', blank=True)
    reuso_cotizacion = models.ManyToManyField(PriceValue, related_name='reuso_cotizacion', blank=True)

    def __str__(self):
        return self.project_data.name
