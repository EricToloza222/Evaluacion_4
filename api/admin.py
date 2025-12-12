from django.contrib import admin
from .models import Cliente, Equipo, Tecnico, PlanMantencion, OrdenTrabajo

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
	list_display = ('rut', 'razon_social', 'giro', 'telefono', 'activo')
	list_filter = ('activo',)
	search_fields = ('rut', 'razon_social', 'giro')
	ordering = ('razon_social',)


@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
	list_display = ('codigo', 'nombre', 'cliente', 'tipo', 'marca', 'activo')
	list_filter = ('tipo', 'activo', 'cliente')
	search_fields = ('codigo', 'nombre', 'numero_serie', 'marca', 'modelo')
	ordering = ('codigo',)


@admin.register(Tecnico)
class TecnicoAdmin(admin.ModelAdmin):
	list_display = ('rut', 'usuario', 'especialidad', 'telefono', 'activo')
	list_filter = ('especialidad', 'activo')
	search_fields = ('rut', 'usuario__username', 'usuario__first_name', 'usuario__last_name')
	ordering = ('usuario__last_name',)


@admin.register(PlanMantencion)
class PlanMantencionAdmin(admin.ModelAdmin):
	list_display = ('nombre', 'equipo', 'frecuencia', 'duracion_estimada', 'activo')
	list_filter = ('frecuencia', 'activo')
	search_fields = ('nombre', 'equipo__codigo', 'equipo__nombre')
	ordering = ('equipo', 'nombre')


@admin.register(OrdenTrabajo)
class OrdenTrabajoAdmin(admin.ModelAdmin):
	list_display = ('codigo', 'equipo', 'tecnico', 'estado', 'prioridad', 'fecha_solicitud')
	list_filter = ('estado', 'prioridad', 'fecha_solicitud')
	search_fields = ('codigo', 'equipo__codigo', 'equipo__nombre', 'tecnico__usuario__username')
	ordering = ('-fecha_solicitud',)
	date_hierarchy = 'fecha_solicitud'
