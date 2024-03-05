from django.db import models
from django.contrib.auth.models import User
# Create your models here.

SYSTEM_CATEGORIES=[
    ('clean_water_system', 'Clean Water'),
    ('waste_water_system', 'Waste Water'),
    ('reuso_water_system', 'Reuso Water'),
]

SYSTEM_CHOICES = [
        ('osmosis', 'Osmosis Inversa'),
        ('suavisador', 'Suavisador'),
        ('filtracion', 'Filtracion'),
        ('pretratamiento', 'Pretratamiento'),
        ('lodosActivados', 'Lodos Activados'),
        ('bioFiltracion', 'BioFiltracion'),
        ('mbbr', 'MBBR'),
        ('osmosisReuso', 'Osmosis Reuso'),
        ('ultrafiltracion', 'Ultrafiltracion'),
        ('daf', 'DAF'),
    ]

SYSTEMS_UNITS=[
    ('gpm','GPM'),
    ('gpd','GPD'),
    ('lts/hr','lts/hr'),
    ('m3/h','m3/h'),
    ('m3/d','m3/d'),
]

CURRENCY_UNITS=[
    ('USD','usd'),
    ('MXN','mxn'),
]

class SystemCategory(models.Model):
    title=models.CharField(max_length=30, choices=SYSTEM_CATEGORIES, null=True, blank=True )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class SystemType(models.Model):
    system_category=models.ForeignKey(SystemCategory, on_delete=models.CASCADE, related_name='system_category' )
    title=models.CharField(max_length=30, choices=SYSTEM_CHOICES, null=True, blank=True )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class IqeaUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100,null=True, blank=True )
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
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



class SystemCotizacion(models.Model):
    system_type=models.ForeignKey(SystemType, on_delete=models.CASCADE, related_name='system_cotizacion',blank=True, null=True )
    flow = models.FloatField(blank=True, null=True)
    unit = models.CharField(max_length=255, blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    currency = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        # project_name = self.cotizacion.project_data.name if self.cotizacion and self.cotizacion.project_data else ""
        return f"{self.system_type} - {self.flow}{self.unit}"


class Cotizacion(models.Model):
    user = models.ForeignKey(IqeaUser, on_delete=models.CASCADE, null=True, blank=True,  db_index=True )
    created = models.DateTimeField(auto_now_add=True)
    project_data = models.ForeignKey(ProjectData, on_delete=models.CASCADE, null=True, blank=True)
    clean_water_system = models.ManyToManyField(SystemCotizacion, related_name='waterCotizacion', blank=True)
    waste_water_system = models.ManyToManyField(SystemCotizacion, related_name='wasteWaterCotizacion', blank=True)
    reuso_water_system = models.ManyToManyField(SystemCotizacion, related_name='reusoCotizacion', blank=True)

    def __str__(self):
        return self.project_data.name


class PreciosReferencia(models.Model):
    system_type=models.ForeignKey(SystemType, on_delete=models.CASCADE, related_name='system_type',blank=True, null=True )
    description=models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.system_type.title


class PrecioRefPoint(models.Model):
    precios_referencia = models.ForeignKey(PreciosReferencia, on_delete=models.CASCADE, related_name='precios_ref_points')
    flujo=models.DecimalField(max_digits=10, decimal_places=2)
    unidad=models.CharField(max_length=10, choices=SYSTEMS_UNITS)
    precioFinal=models.DecimalField(max_digits=10, decimal_places=2)
    currency=models.CharField(max_length=4, choices=CURRENCY_UNITS, blank=True, null=True)
    consideraciones=models.CharField(max_length=255, blank=True, null=True)
