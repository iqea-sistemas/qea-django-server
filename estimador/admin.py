from django.contrib import admin
from .models import *
# Register your models here.



class IqeaUserAdmin(admin.ModelAdmin):

    readonly_fields = ('created', )
    list_display = ('name', 'email', 'company', 'created') #visualizar columnas
    ordering = ('-created', ) #ordenar listas
    search_fields = ('company',)  #buscador

class ProjectsAdmin(admin.ModelAdmin):

    readonly_fields = ('created', )
    list_display = ('project_name', 'user', 'location', 'created') #visualizar columnas
    ordering = ('-created', ) #ordenar listas


admin.site.register(IqeaUser, IqeaUserAdmin)
admin.site.register(Projects, ProjectsAdmin)

