from django.contrib import admin
from .models import *
# Register your models here.



class IqeaUserAdmin(admin.ModelAdmin):

    readonly_fields = ('created', )
    list_display = ('name', 'email', 'company', 'created') #visualizar columnas
    ordering = ('-created', ) #ordenar listas
    search_fields = ('company',)  #buscador



class CotizacionAdmin(admin.ModelAdmin):
    list_display = ( 'user', 'project_data', 'created') #visualizar columnas

class ProjectDataAdmin(admin.ModelAdmin):
    list_display = ( 'name', 'location') #visualizar columnas

class WaterSystemAdmin(admin.ModelAdmin):
    list_display = ( 'system', 'flow') #visualizar columnas

class WasteWaterSystemAdmin(admin.ModelAdmin):
    list_display = ( 'system', 'flow') #visualizar columnas

class ReusoSystemAdmin(admin.ModelAdmin):
    list_display = ( 'system', 'flow') #visualizar columnas

admin.site.register(Cotizacion, CotizacionAdmin)
admin.site.register(ProjectData, ProjectDataAdmin)
admin.site.register(WaterSystem, WaterSystemAdmin)
admin.site.register(WasteWaterSystem, WasteWaterSystemAdmin)
admin.site.register(ReusoSystem, ReusoSystemAdmin)

admin.site.register(IqeaUser, IqeaUserAdmin)

