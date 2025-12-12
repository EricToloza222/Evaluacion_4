from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Cliente, Equipo, Tecnico, PlanMantencion, OrdenTrabajo


class ClienteSerializer(serializers.ModelSerializer):
	"""Serializer para el modelo Cliente."""
	class Meta:
		model = Cliente
		fields = ['id', 'rut', 'razon_social', 'giro', 'direccion', 'telefono', 'email', 'fecha_registro', 'activo']
		read_only_fields = ['id', 'fecha_registro']


class EquipoSerializer(serializers.ModelSerializer):
	"""Serializer para el modelo Equipo."""
	cliente_nombre = serializers.CharField(source='cliente.razon_social', read_only=True)
	
	class Meta:
		model = Equipo
		fields = [
			'id', 'cliente', 'cliente_nombre', 'codigo', 'nombre', 'tipo', 
			'marca', 'modelo', 'numero_serie', 'fecha_instalacion', 
			'ubicacion', 'ficha_tecnica', 'activo'
		]
		read_only_fields = ['id']


class TecnicoSerializer(serializers.ModelSerializer):
	"""Serializer para el modelo Técnico."""
	usuario_nombre = serializers.CharField(source='usuario.get_full_name', read_only=True)
	usuario_email = serializers.CharField(source='usuario.email', read_only=True)
	
	class Meta:
		model = Tecnico
		fields = [
			'id', 'usuario', 'usuario_nombre', 'usuario_email', 'rut', 
			'especialidad', 'telefono', 'fecha_contratacion', 'activo'
		]
		read_only_fields = ['id']


class PlanMantencionSerializer(serializers.ModelSerializer):
	"""Serializer para el modelo PlanMantencion."""
	equipo_codigo = serializers.CharField(source='equipo.codigo', read_only=True)
	
	class Meta:
		model = PlanMantencion
		fields = [
			'id', 'equipo', 'equipo_codigo', 'nombre', 'descripcion', 
			'frecuencia', 'duracion_estimada', 'procedimiento', 'activo'
		]
		read_only_fields = ['id']


class OrdenTrabajoSerializer(serializers.ModelSerializer):
	"""Serializer para el modelo OrdenTrabajo."""
	equipo_codigo = serializers.CharField(source='equipo.codigo', read_only=True)
	tecnico_nombre = serializers.CharField(source='tecnico.usuario.get_full_name', read_only=True)
	plan_nombre = serializers.CharField(source='plan_mantencion.nombre', read_only=True)
	
	class Meta:
		model = OrdenTrabajo
		fields = [
			'id', 'equipo', 'equipo_codigo', 'tecnico', 'tecnico_nombre', 
			'plan_mantencion', 'plan_nombre', 'codigo', 'descripcion', 
			'fecha_solicitud', 'fecha_programada', 'fecha_inicio', 'fecha_fin', 
			'estado', 'prioridad', 'observaciones', 'costo_estimado', 'costo_real'
		]
		read_only_fields = ['id', 'fecha_solicitud']


class UserSerializer(serializers.ModelSerializer):
	"""Serializer para el modelo User."""
	class Meta:
		model = User
		fields = ['id', 'username', 'email', 'first_name', 'last_name']
		read_only_fields = ['id']
