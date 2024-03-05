from django.contrib import admin
from .models import *
# Register your models here.



class IqeaUserAdmin(admin.ModelAdmin):
    readonly_fields = ('created', )
    list_display = ('name', 'email', 'company', 'created') #visualizar columnas
    ordering = ('-created', ) #ordenar listas
    search_fields = ('company',)  #buscador

class SystemCategoryAdmin(admin.ModelAdmin):
    list_display = ( 'id','title', ) #visualizar columnas

class SystemTypeAdmin(admin.ModelAdmin):
    list_display = ( 'id','title',) #visualizar columnas


class SystemCotizacionAdmin(admin.ModelAdmin):
    list_display = ( 'get_system_category','get_system_type', 'flow') #visualizar columnas
    def get_system_type(self, obj):
        return obj.system_type.title
    get_system_type.short_description = 'System Type'

    def get_system_category(self, obj):
        return obj.system_type.system_category.title
    get_system_type.short_description = 'System Category'

class CotizacionAdmin(admin.ModelAdmin):
    list_display = ( 'user', 'project_data', 'created') #visualizar columnas

class ProjectDataAdmin(admin.ModelAdmin):
    list_display = ( 'name', 'location') #visualizar columnas

# class WaterSystemAdmin(admin.ModelAdmin):
#     list_display = ( 'system', 'flow') #visualizar columnas

# class WasteWaterSystemAdmin(admin.ModelAdmin):
#     list_display = ( 'system', 'flow') #visualizar columnas

# class ReusoSystemAdmin(admin.ModelAdmin):
#     list_display = ( 'system', 'flow') #visualizar columnas


class PreciosReferenciaAdmin(admin.ModelAdmin):
    list_display = ( 'system_type', 'description') #visualizar columnas



class PrecioRefPointAdmin(admin.ModelAdmin):
    list_display = ( 'get_system_type','flujo', 'unidad', 'precioFinal', 'currency') #visualizar columnas
    def get_system_type(self, obj):
        return obj.precios_referencia.system_type

    get_system_type.short_description = 'System Type'

admin.site.register(SystemCategory, SystemCategoryAdmin)
admin.site.register(SystemType, SystemTypeAdmin)


admin.site.register(SystemCotizacion, SystemCotizacionAdmin)

admin.site.register(Cotizacion, CotizacionAdmin)
admin.site.register(ProjectData, ProjectDataAdmin)
# admin.site.register(WaterSystem, WaterSystemAdmin)
# admin.site.register(WasteWaterSystem, WasteWaterSystemAdmin)
# admin.site.register(ReusoSystem, ReusoSystemAdmin)

admin.site.register(IqeaUser, IqeaUserAdmin)
admin.site.register(PreciosReferencia, PreciosReferenciaAdmin)
admin.site.register(PrecioRefPoint, PrecioRefPointAdmin)

