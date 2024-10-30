from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Direccion, Servicio, SubServicio, Medico, Historial

# Registrar los modelos con funcionalidades de importación y exportación

@admin.register(Direccion)
class DireccionAdmin(ImportExportModelAdmin):
    list_display = ('direccion', 'ciudad', 'estado', 'codigo_postal')
    search_fields = ('direccion', 'ciudad', 'estado', 'codigo_postal')

@admin.register(Servicio)
class ServicioAdmin(ImportExportModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(SubServicio)
class SubServicioAdmin(ImportExportModelAdmin):
    list_display = ('servicio', 'nombre')
    search_fields = ('nombre', 'servicio__nombre')
    list_filter = ('servicio',)

@admin.register(Medico)
class MedicoAdmin(ImportExportModelAdmin):
    list_display = ('nombre', 'apellido', 'matricula')
    search_fields = ('nombre', 'apellido', 'matricula')
    filter_horizontal = ('servicios', 'subservicios')  # Para seleccionar servicios y subservicios fácilmente

@admin.register(Historial)
class HistorialAdmin(ImportExportModelAdmin):
    list_display = ('user', 'subservicio', 'medico', 'direccion', 'fecha')
    search_fields = ('user__username', 'subservicio__nombre', 'medico__nombre', 'direccion__direccion')
    list_filter = ('fecha', 'medico')
