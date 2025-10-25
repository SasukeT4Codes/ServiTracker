from django.contrib import admin
from .models import (
    Queja,
    TipoFalla,
    EstadoQueja,
    Ubicacion,
    ComentarioQueja
)

@admin.register(Queja)
class QuejaAdmin(admin.ModelAdmin):
    list_display = ('id', 'ciudadano', 'tipo_falla', 'estado', 'fecha_reporte', 'fecha_resolucion')
    list_filter = ('estado', 'tipo_falla', 'fecha_reporte')
    search_fields = ('ciudadano__usuario__username', 'descripcion')
    date_hierarchy = 'fecha_reporte'
    ordering = ('-fecha_reporte',)

@admin.register(TipoFalla)
class TipoFallaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(EstadoQueja)
class EstadoQuejaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Ubicacion)
class UbicacionAdmin(admin.ModelAdmin):
    list_display = ('direccion', 'barrio', 'ciudadano')
    search_fields = ('direccion', 'barrio', 'ciudadano__usuario__username')

@admin.register(ComentarioQueja)
class ComentarioQuejaAdmin(admin.ModelAdmin):
    list_display = ('queja', 'autor', 'fecha')
    search_fields = ('autor', 'mensaje')
    date_hierarchy = 'fecha'
