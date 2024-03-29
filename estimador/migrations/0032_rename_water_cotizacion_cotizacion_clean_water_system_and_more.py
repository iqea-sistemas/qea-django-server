# Generated by Django 5.0.1 on 2024-03-01 18:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estimador', '0031_alter_preciorefpoint_currency_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cotizacion',
            old_name='water_cotizacion',
            new_name='clean_water_system',
        ),
        migrations.RenameField(
            model_name='cotizacion',
            old_name='reuso_cotizacion',
            new_name='reuso_water_system',
        ),
        migrations.RenameField(
            model_name='cotizacion',
            old_name='waste_water_cotizacion',
            new_name='waste_water_system',
        ),
        migrations.AlterField(
            model_name='preciorefpoint',
            name='unidad',
            field=models.CharField(choices=[('gpm', 'GPM'), ('gpd', 'GPD'), ('lts/hr', 'lts/hr'), ('m3/h', 'm3/h'), ('m3/d', 'm3/d')], max_length=10),
        ),
        migrations.AlterField(
            model_name='systemcategory',
            name='title',
            field=models.CharField(blank=True, choices=[('clean_water_system', 'Clean Water'), ('waste_water_system', 'Waste Water'), ('reuso_water_system', 'Reuso Water')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='systemtype',
            name='title',
            field=models.CharField(blank=True, choices=[('osmosis', 'Osmosis Inversa'), ('suavisador', 'Suavisador'), ('filtracion', 'Filtracion'), ('pretratamiento', 'Pretratamiento'), ('lodosActivados', 'Lodos Activados'), ('bioFiltracion', 'BioFiltracion'), ('mbbr', 'MBBR'), ('osmosisReuso', 'Osmosis Reuso'), ('ultrafiltracion', 'Ultrafiltracion')], max_length=30, null=True),
        ),
        migrations.CreateModel(
            name='SystemCotizacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flow', models.FloatField(blank=True, null=True)),
                ('unit', models.CharField(blank=True, max_length=255, null=True)),
                ('price', models.FloatField(blank=True, null=True)),
                ('currency', models.CharField(blank=True, max_length=255, null=True)),
                ('system_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='system_cotizacion', to='estimador.systemtype')),
            ],
        ),
    ]
