from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Cliente(models.Model):
	"""Modelo para gestionar empresas clientes."""
	rut = models.CharField(max_length=12, unique=True, verbose_name="RUT")
	razon_social = models.CharField(max_length=200, verbose_name="Razón Social")
	giro = models.CharField(max_length=200, verbose_name="Giro Comercial")
	direccion = models.CharField(max_length=300, verbose_name="Dirección")
	telefono = models.CharField(max_length=20, verbose_name="Teléfono")
	email = models.EmailField(verbose_name="Correo Electrónico")
	fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")
	activo = models.BooleanField(default=True, verbose_name="Activo")

	class Meta:
		verbose_name = "Cliente"
		verbose_name_plural = "Clientes"
		ordering = ['razon_social']

	def __str__(self):
		return f"{self.razon_social} ({self.rut})"


class Equipo(models.Model):
	"""Modelo para gestionar equipos vinculados a clientes."""
	TIPO_EQUIPO_CHOICES = [
		('MAQ', 'Máquina'),
		('EQU', 'Equipo Electrónico'),
		('SIS', 'Sistema'),
		('VEH', 'Vehículo'),
		('OTR', 'Otro'),
	]

	cliente = models.ForeignKey(
		Cliente, 
		on_delete=models.CASCADE, 
		related_name='equipos',
		verbose_name="Cliente Dueño"
	)
	codigo = models.CharField(max_length=50, unique=True, verbose_name="Código del Equipo")
	nombre = models.CharField(max_length=200, verbose_name="Nombre del Equipo")
	tipo = models.CharField(
		max_length=3, 
		choices=TIPO_EQUIPO_CHOICES, 
		default='MAQ',
		verbose_name="Tipo de Equipo"
	)
	marca = models.CharField(max_length=100, verbose_name="Marca")
	modelo = models.CharField(max_length=100, verbose_name="Modelo")
	numero_serie = models.CharField(max_length=100, unique=True, verbose_name="Número de Serie")
	fecha_instalacion = models.DateField(verbose_name="Fecha de Instalación")
	ubicacion = models.CharField(max_length=300, verbose_name="Ubicación Física")
	ficha_tecnica = models.TextField(blank=True, verbose_name="Ficha Técnica")
	activo = models.BooleanField(default=True, verbose_name="Activo")

	class Meta:
		verbose_name = "Equipo"
		verbose_name_plural = "Equipos"
		ordering = ['codigo']

	def __str__(self):
		return f"{self.codigo} - {self.nombre} ({self.cliente.razon_social})"


class Tecnico(models.Model):
	"""Modelo para gestionar técnicos responsables de mantenciones."""
	ESPECIALIDAD_CHOICES = [
		('MEC', 'Mecánico'),
		('ELE', 'Eléctrico'),
		('ELE', 'Electrónico'),
		('SIS', 'Sistemas'),
		('GEN', 'General'),
	]

	usuario = models.OneToOneField(
		User, 
		on_delete=models.CASCADE, 
		related_name='tecnico',
		verbose_name="Usuario Asociado"
	)
	rut = models.CharField(max_length=12, unique=True, verbose_name="RUT")
	especialidad = models.CharField(
		max_length=3, 
		choices=ESPECIALIDAD_CHOICES, 
		default='GEN',
		verbose_name="Especialidad"
	)
	telefono = models.CharField(max_length=20, verbose_name="Teléfono")
	fecha_contratacion = models.DateField(verbose_name="Fecha de Contratación")
	activo = models.BooleanField(default=True, verbose_name="Activo")

	class Meta:
		verbose_name = "Técnico"
		verbose_name_plural = "Técnicos"
		ordering = ['usuario__last_name']

	def __str__(self):
		return f"{self.usuario.get_full_name()} ({self.especialidad})"


class PlanMantencion(models.Model):
	"""Modelo para gestionar planes preventivos de mantención asociados a equipos."""
	FRECUENCIA_CHOICES = [
		('DIA', 'Diaria'),
		('SEM', 'Semanal'),
		('MEN', 'Mensual'),
		('BIM', 'Bimestral'),
		('TRI', 'Trimestral'),
		('SEM', 'Semestral'),
		('ANU', 'Anual'),
	]

	equipo = models.ForeignKey(
		Equipo, 
		on_delete=models.CASCADE, 
		related_name='planes_mantencion',
		verbose_name="Equipo"
	)
	nombre = models.CharField(max_length=200, verbose_name="Nombre del Plan")
	descripcion = models.TextField(verbose_name="Descripción")
	frecuencia = models.CharField(
		max_length=3, 
		choices=FRECUENCIA_CHOICES, 
		default='MEN',
		verbose_name="Frecuencia"
	)
	duracion_estimada = models.PositiveIntegerField(
		verbose_name="Duración Estimada (horas)",
		validators=[MinValueValidator(1)]
	)
	procedimiento = models.TextField(verbose_name="Procedimiento a Seguir")
	activo = models.BooleanField(default=True, verbose_name="Activo")

	class Meta:
		verbose_name = "Plan de Mantención"
		verbose_name_plural = "Planes de Mantención"
		ordering = ['equipo', 'nombre']
		unique_together = ['equipo', 'nombre']

	def __str__(self):
		return f"{self.nombre} - {self.equipo.codigo}"


class OrdenTrabajo(models.Model):
	"""Modelo para gestionar órdenes de trabajo de mantención."""
	ESTADO_CHOICES = [
		('PEN', 'Pendiente'),
		('PRO', 'En Proceso'),
		('FIN', 'Finalizada'),
		('CAN', 'Cancelada'),
	]

	PRIORIDAD_CHOICES = [
		('BAJ', 'Baja'),
		('MED', 'Media'),
		('ALT', 'Alta'),
		('URG', 'Urgente'),
	]

	equipo = models.ForeignKey(
		Equipo, 
		on_delete=models.CASCADE, 
		related_name='ordenes_trabajo',
		verbose_name="Equipo"
	)
	tecnico = models.ForeignKey(
		Tecnico, 
		on_delete=models.SET_NULL, 
		null=True, 
		blank=True,
		related_name='ordenes_trabajo',
		verbose_name="Técnico Asignado"
	)
	plan_mantencion = models.ForeignKey(
		PlanMantencion, 
		on_delete=models.SET_NULL, 
		null=True, 
		blank=True,
		related_name='ordenes_trabajo',
		verbose_name="Plan de Mantención Asociado"
	)
	codigo = models.CharField(max_length=50, unique=True, verbose_name="Código de Orden")
	descripcion = models.TextField(verbose_name="Descripción del Trabajo")
	fecha_solicitud = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Solicitud")
	fecha_programada = models.DateField(verbose_name="Fecha Programada")
	fecha_inicio = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Inicio Real")
	fecha_fin = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Fin Real")
	estado = models.CharField(
		max_length=3, 
		choices=ESTADO_CHOICES, 
		default='PEN',
		verbose_name="Estado"
	)
	prioridad = models.CharField(
		max_length=3, 
		choices=PRIORIDAD_CHOICES, 
		default='MED',
		verbose_name="Prioridad"
	)
	observaciones = models.TextField(blank=True, verbose_name="Observaciones")
	costo_estimado = models.DecimalField(
		max_digits=10, 
		decimal_places=2, 
		default=0.00,
		verbose_name="Costo Estimado"
	)
	costo_real = models.DecimalField(
		max_digits=10, 
		decimal_places=2, 
		null=True, 
		blank=True,
		verbose_name="Costo Real"
	)

	class Meta:
		verbose_name = "Orden de Trabajo"
		verbose_name_plural = "Órdenes de Trabajo"
		ordering = ['-fecha_solicitud']

	def __str__(self):
		return f"{self.codigo} - {self.equipo.codigo} ({self.estado})"
