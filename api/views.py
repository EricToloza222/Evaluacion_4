from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.contrib.auth.models import User
from .models import Cliente, Equipo, Tecnico, PlanMantencion, OrdenTrabajo
from .serializers import (
	ClienteSerializer, EquipoSerializer, TecnicoSerializer, 
	PlanMantencionSerializer, OrdenTrabajoSerializer, UserSerializer
)


class ClienteViewSet(viewsets.ModelViewSet):
	"""
	ViewSet para gestionar clientes.
	- GET /api/clientes/ : Listar todos los clientes
	- POST /api/clientes/ : Crear nuevo cliente (requiere autenticación)
	- GET /api/clientes/{id}/ : Obtener detalles de un cliente
	- PUT /api/clientes/{id}/ : Actualizar cliente (requiere autenticación)
	- DELETE /api/clientes/{id}/ : Eliminar cliente (requiere autenticación)
	"""
	queryset = Cliente.objects.all()
	serializer_class = ClienteSerializer
	permission_classes = [IsAuthenticatedOrReadOnly]
	filterset_fields = ['activo']
	search_fields = ['razon_social', 'rut', 'email']
	ordering_fields = ['razon_social', 'fecha_registro']
	ordering = ['razon_social']


class EquipoViewSet(viewsets.ModelViewSet):
	"""
	ViewSet para gestionar equipos.
	- GET /api/equipos/ : Listar todos los equipos
	- POST /api/equipos/ : Crear nuevo equipo (requiere autenticación)
	- GET /api/equipos/{id}/ : Obtener detalles de un equipo
	- PUT /api/equipos/{id}/ : Actualizar equipo (requiere autenticación)
	- DELETE /api/equipos/{id}/ : Eliminar equipo (requiere autenticación)
	"""
	queryset = Equipo.objects.all()
	serializer_class = EquipoSerializer
	permission_classes = [IsAuthenticatedOrReadOnly]
	filterset_fields = ['cliente', 'tipo', 'activo']
	search_fields = ['codigo', 'nombre', 'marca', 'numero_serie']
	ordering_fields = ['codigo', 'fecha_instalacion']
	ordering = ['codigo']

	@action(detail=True, methods=['get'], permission_classes=[IsAuthenticatedOrReadOnly])
	def ficha_tecnica(self, request, pk=None):
		"""Endpoint para obtener la ficha técnica de un equipo."""
		equipo = self.get_object()
		return Response({
			'codigo': equipo.codigo,
			'nombre': equipo.nombre,
			'marca': equipo.marca,
			'modelo': equipo.modelo,
			'numero_serie': equipo.numero_serie,
			'tipo': equipo.tipo,
			'ficha_tecnica': equipo.ficha_tecnica,
			'fecha_instalacion': equipo.fecha_instalacion,
			'ubicacion': equipo.ubicacion,
		})


class TecnicoViewSet(viewsets.ModelViewSet):
	"""
	ViewSet para gestionar técnicos.
	- GET /api/tecnicos/ : Listar todos los técnicos
	- POST /api/tecnicos/ : Crear nuevo técnico (requiere autenticación)
	- GET /api/tecnicos/{id}/ : Obtener detalles de un técnico
	- PUT /api/tecnicos/{id}/ : Actualizar técnico (requiere autenticación)
	- DELETE /api/tecnicos/{id}/ : Eliminar técnico (requiere autenticación)
	"""
	queryset = Tecnico.objects.all()
	serializer_class = TecnicoSerializer
	permission_classes = [IsAuthenticatedOrReadOnly]
	filterset_fields = ['especialidad', 'activo']
	search_fields = ['usuario__last_name', 'usuario__first_name', 'rut']
	ordering_fields = ['usuario__last_name', 'fecha_contratacion']
	ordering = ['usuario__last_name']


class PlanMantencionViewSet(viewsets.ModelViewSet):
	"""
	ViewSet para gestionar planes de mantención.
	- GET /api/planes/ : Listar todos los planes
	- POST /api/planes/ : Crear nuevo plan (requiere autenticación)
	- GET /api/planes/{id}/ : Obtener detalles de un plan
	- PUT /api/planes/{id}/ : Actualizar plan (requiere autenticación)
	- DELETE /api/planes/{id}/ : Eliminar plan (requiere autenticación)
	"""
	queryset = PlanMantencion.objects.all()
	serializer_class = PlanMantencionSerializer
	permission_classes = [IsAuthenticatedOrReadOnly]
	filterset_fields = ['equipo', 'frecuencia', 'activo']
	search_fields = ['nombre', 'equipo__codigo']
	ordering_fields = ['nombre', 'frecuencia']
	ordering = ['nombre']


class OrdenTrabajoViewSet(viewsets.ModelViewSet):
	"""
	ViewSet para gestionar órdenes de trabajo.
	- GET /api/ordenes/ : Listar todas las órdenes
	- POST /api/ordenes/ : Crear nueva orden (requiere autenticación)
	- GET /api/ordenes/{id}/ : Obtener detalles de una orden
	- PUT /api/ordenes/{id}/ : Actualizar orden (requiere autenticación)
	- DELETE /api/ordenes/{id}/ : Eliminar orden (requiere autenticación)
	- GET /api/ordenes/{id}/cambiar_estado/ : Cambiar estado de la orden
	"""
	queryset = OrdenTrabajo.objects.all()
	serializer_class = OrdenTrabajoSerializer
	permission_classes = [IsAuthenticatedOrReadOnly]
	filterset_fields = ['equipo', 'tecnico', 'estado', 'prioridad']
	search_fields = ['codigo', 'descripcion', 'equipo__codigo']
	ordering_fields = ['fecha_solicitud', 'fecha_programada', 'prioridad']
	ordering = ['-fecha_solicitud']

	@action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
	def cambiar_estado(self, request, pk=None):
		"""Endpoint para cambiar el estado de una orden de trabajo."""
		orden = self.get_object()
		nuevo_estado = request.data.get('estado')
		
		estados_validos = [choice[0] for choice in OrdenTrabajo.ESTADO_CHOICES]
		
		if nuevo_estado not in estados_validos:
			return Response(
				{'error': f'Estado inválido. Estados válidos: {estados_validos}'},
				status=status.HTTP_400_BAD_REQUEST
			)
		
		orden.estado = nuevo_estado
		orden.save()
		
		serializer = self.get_serializer(orden)
		return Response(serializer.data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
	"""
	ViewSet para gestionar usuarios (solo lectura).
	- GET /api/usuarios/ : Listar todos los usuarios
	- GET /api/usuarios/{id}/ : Obtener detalles de un usuario
	"""
	queryset = User.objects.all()
	serializer_class = UserSerializer
	permission_classes = [IsAuthenticated]
	search_fields = ['username', 'email', 'first_name', 'last_name']
	ordering_fields = ['username', 'date_joined']
	ordering = ['username']
