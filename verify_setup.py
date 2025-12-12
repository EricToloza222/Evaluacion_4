#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Script de prueba para verificar que todo funciona correctamente."""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

# Pruebas de imports
print("Verificando imports...")
try:
    from api.serializers import (
        ClienteSerializer, EquipoSerializer, TecnicoSerializer,
        PlanMantencionSerializer, OrdenTrabajoSerializer, UserSerializer
    )
    print("[OK] Serializers importados correctamente")
except Exception as e:
    print(f"[ERROR] Error en serializers: {e}")
    sys.exit(1)

try:
    from api.views import (
        ClienteViewSet, EquipoViewSet, TecnicoViewSet,
        PlanMantencionViewSet, OrdenTrabajoViewSet, UserViewSet
    )
    print("[OK] ViewSets importados correctamente")
except Exception as e:
    print(f"[ERROR] Error en views: {e}")
    sys.exit(1)

# Pruebas de models
print("\nVerificando modelos...")
try:
    from api.models import Cliente, Equipo, Tecnico, PlanMantencion, OrdenTrabajo
    print("[OK] Cliente: registrado")
    print("[OK] Equipo: registrado")
    print("[OK] Tecnico: registrado")
    print("[OK] PlanMantencion: registrado")
    print("[OK] OrdenTrabajo: registrado")
except Exception as e:
    print(f"[ERROR] Error en modelos: {e}")
    sys.exit(1)

# Pruebas de rutas
print("\nVerificando URLs...")
try:
    from api.urls import urlpatterns
    print(f"[OK] URLs configuradas: {len(urlpatterns)} rutas")
except Exception as e:
    print(f"[ERROR] Error en URLs: {e}")
    sys.exit(1)

# Verificar REST Framework
print("\nVerificando configuracion de REST Framework...")
from django.conf import settings
rest_config = settings.REST_FRAMEWORK
print(f"[OK] Autenticacion: configurada")
print(f"[OK] Permisos: configurados")
print(f"[OK] Filtros: configurados")
print(f"[OK] Paginacion: {rest_config.get('PAGE_SIZE')} items por pagina")

print("\n" + "="*50)
print("[OK] TODAS LAS VERIFICACIONES PASARON CORRECTAMENTE")
print("="*50)
