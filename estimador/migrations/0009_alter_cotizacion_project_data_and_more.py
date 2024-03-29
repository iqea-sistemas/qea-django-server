# Generated by Django 5.0.1 on 2024-02-05 20:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estimador', '0008_remove_cotizacion_reuso_cotizacion_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cotizacion',
            name='project_data',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='estimador.projectdata'),
        ),
        migrations.AlterField(
            model_name='cotizacion',
            name='reuso_cotizacion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reuso_cotizacion', to='estimador.pricevalue'),
        ),
        migrations.AlterField(
            model_name='cotizacion',
            name='waste_water_cotizacion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='waste_water_cotizacion', to='estimador.pricevalue'),
        ),
        migrations.AlterField(
            model_name='cotizacion',
            name='water_cotizacion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='water_cotizacion', to='estimador.pricevalue'),
        ),
    ]
