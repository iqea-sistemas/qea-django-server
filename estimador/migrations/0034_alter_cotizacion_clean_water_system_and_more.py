# Generated by Django 5.0.1 on 2024-03-01 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estimador', '0033_cotizacion_system_cotizacion_systemcotizacion_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cotizacion',
            name='clean_water_system',
            field=models.ManyToManyField(blank=True, related_name='waterCotizacion', to='estimador.systemcotizacion'),
        ),
        migrations.AlterField(
            model_name='cotizacion',
            name='reuso_water_system',
            field=models.ManyToManyField(blank=True, related_name='reusoCotizacion', to='estimador.systemcotizacion'),
        ),
        migrations.AlterField(
            model_name='cotizacion',
            name='waste_water_system',
            field=models.ManyToManyField(blank=True, related_name='wasteWaterCotizacion', to='estimador.systemcotizacion'),
        ),
    ]
