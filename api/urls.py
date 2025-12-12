from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
	ClienteViewSet, EquipoViewSet, TecnicoViewSet,
	PlanMantencionViewSet, OrdenTrabajoViewSet, UserViewSet
)

# Crear el router y registrar los ViewSets
router = DefaultRouter()
router.register(r'clientes', ClienteViewSet, basename='cliente')
router.register(r'equipos', EquipoViewSet, basename='equipo')
router.register(r'tecnicos', TecnicoViewSet, basename='tecnico')
router.register(r'planes', PlanMantencionViewSet, basename='plan-mantencion')
router.register(r'ordenes', OrdenTrabajoViewSet, basename='orden-trabajo')
router.register(r'usuarios', UserViewSet, basename='usuario')

# Las URLs son generadas automáticamente por el router
urlpatterns = [
	path('', include(router.urls)),
]
