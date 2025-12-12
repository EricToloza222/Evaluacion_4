# API de Gestión de Mantenimiento Industrial

API RESTful desarrollada con Django REST Framework para la gestión de clientes, equipos, técnicos, planes de mantención y órdenes de trabajo en empresas de mantenimiento industrial.

## Descripción del Proyecto

Este proyecto es una API REST segura que permite registrar, consultar y administrar información de:
- **Clientes**: Empresas que requieren servicios de mantenimiento
- **Equipos**: Máquinas y sistemas de los clientes
- **Técnicos**: Profesionales responsables de las mantenciones
- **Planes de Mantención**: Programas preventivos asociados a equipos
- **Órdenes de Trabajo**: Servicios de mantenimiento solicitados

## Contexto
Proyecto desarrollado para la Evaluación N°4 de la asignatura Programación Backend (TI2041) de Tecnologías de la Información y Ciberseguridad, Primavera 2025.

## Estado Actual
- ✅ Proyecto Django configurado
- ✅ Django REST Framework instalado y configurado
- ✅ Modelos ORM implementados (5 entidades principales)
- ✅ Serializers creados para todas las entidades
- ✅ ViewSets implementados con CRUD completo
- ✅ Autenticación JWT configurada
- ✅ Sistema de permisos implementado
- ✅ API navegable habilitada
- ✅ Filtrado, búsqueda y ordenamiento configurados

## Requisitos

### Dependencias Principales
- Python 3.14+
- Django 6.0
- Django REST Framework 3.16.1
- Django REST Framework SimpleJWT 5.3.0
- django-filter 25.1

### Instalación de Dependencias

```bash
pip install -r requirements.txt
```

## Pasos para Ejecutar la API

### 1. Configuración Inicial
```bash
# Clonar o descargar el proyecto
cd Evaluacion_4-main

# Crear y activar un entorno virtual (opcional pero recomendado)
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 2. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 3. Realizar Migraciones
```bash
python manage.py migrate
```

### 4. Crear Usuario Administrador
```bash
python manage.py createsuperuser
# Sigue las instrucciones para crear el usuario
```

### 5. Ejecutar el Servidor
```bash
python manage.py runserver
```

El servidor estará disponible en: `http://127.0.0.1:8000/`

## Endpoints de la API

### Base URL: `http://127.0.0.1:8000/api/`

#### 1. Gestión de Clientes
- **GET** `/api/clientes/` - Listar todos los clientes
- **POST** `/api/clientes/` - Crear nuevo cliente (requiere autenticación)
- **GET** `/api/clientes/{id}/` - Obtener detalles de un cliente
- **PUT** `/api/clientes/{id}/` - Actualizar cliente (requiere autenticación)
- **DELETE** `/api/clientes/{id}/` - Eliminar cliente (requiere autenticación)

**Ejemplo GET (sin autenticación):**
```
GET http://127.0.0.1:8000/api/clientes/
```

**Ejemplo POST (requiere token JWT):**
```
POST http://127.0.0.1:8000/api/clientes/
Content-Type: application/json
Authorization: Bearer <token_jwt>

{
    "rut": "12345678-9",
    "razon_social": "Empresa Ejemplo S.A.",
    "giro": "Mantenimiento Industrial",
    "direccion": "Calle Principal 123",
    "telefono": "+56912345678",
    "email": "contacto@empresa.cl"
}
```

#### 2. Gestión de Equipos
- **GET** `/api/equipos/` - Listar todos los equipos
- **POST** `/api/equipos/` - Crear nuevo equipo (requiere autenticación)
- **GET** `/api/equipos/{id}/` - Obtener detalles de un equipo
- **GET** `/api/equipos/{id}/ficha_tecnica/` - Obtener ficha técnica del equipo
- **PUT** `/api/equipos/{id}/` - Actualizar equipo (requiere autenticación)
- **DELETE** `/api/equipos/{id}/` - Eliminar equipo (requiere autenticación)

#### 3. Gestión de Técnicos
- **GET** `/api/tecnicos/` - Listar todos los técnicos
- **POST** `/api/tecnicos/` - Crear nuevo técnico (requiere autenticación)
- **GET** `/api/tecnicos/{id}/` - Obtener detalles de un técnico
- **PUT** `/api/tecnicos/{id}/` - Actualizar técnico (requiere autenticación)
- **DELETE** `/api/tecnicos/{id}/` - Eliminar técnico (requiere autenticación)

#### 4. Gestión de Planes de Mantención
- **GET** `/api/planes/` - Listar todos los planes
- **POST** `/api/planes/` - Crear nuevo plan (requiere autenticación)
- **GET** `/api/planes/{id}/` - Obtener detalles de un plan
- **PUT** `/api/planes/{id}/` - Actualizar plan (requiere autenticación)
- **DELETE** `/api/planes/{id}/` - Eliminar plan (requiere autenticación)

#### 5. Gestión de Órdenes de Trabajo
- **GET** `/api/ordenes/` - Listar todas las órdenes
- **POST** `/api/ordenes/` - Crear nueva orden (requiere autenticación)
- **GET** `/api/ordenes/{id}/` - Obtener detalles de una orden
- **POST** `/api/ordenes/{id}/cambiar_estado/` - Cambiar estado de la orden (requiere autenticación)
- **PUT** `/api/ordenes/{id}/` - Actualizar orden (requiere autenticación)
- **DELETE** `/api/ordenes/{id}/` - Eliminar orden (requiere autenticación)

#### 6. Autenticación
- **POST** `/api/token/` - Obtener token JWT
- **POST** `/api/token/refresh/` - Refrescar token JWT

**Ejemplo obtener token:**
```
POST http://127.0.0.1:8000/api/token/
Content-Type: application/json

{
    "username": "admin",
    "password": "tu_contraseña"
}

Respuesta:
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

## Características de Seguridad

### Autenticación
- Sistema de autenticación JWT (JSON Web Tokens)
- Soporte para autenticación por sesión
- Tokens con tiempo de expiración configurable

### Control de Acceso
- **Usuarios no autenticados**: Pueden consultar (lectura) todos los datos
- **Usuarios autenticados**: Pueden crear, modificar y eliminar registros
- Permisos basados en roles y autenticación

### Respuestas JSON
- Todas las respuestas en formato JSON
- Códigos HTTP estándar (200, 201, 400, 401, 403, 404, etc.)
- Mensajes de error descriptivos

## Capacidades Avanzadas

### Filtrado
Los endpoints soportan filtrado por parámetros específicos:
```
GET /api/clientes/?activo=true
GET /api/equipos/?tipo=MAQ&activo=true
GET /api/ordenes/?estado=PEN&prioridad=ALT
```

### Búsqueda
Búsqueda por texto en múltiples campos:
```
GET /api/clientes/?search=empresa
GET /api/equipos/?search=codigo
GET /api/ordenes/?search=descripcion
```

### Ordenamiento
Ordenar resultados por campos específicos:
```
GET /api/clientes/?ordering=razon_social
GET /api/ordenes/?ordering=-fecha_solicitud
```

### Paginación
Resultados paginados a 20 items por página:
```
GET /api/clientes/?page=1
GET /api/clientes/?page=2
```

## Estructura de Modelos

### Cliente
- RUT (único)
- Razón Social
- Giro Comercial
- Dirección
- Teléfono
- Email
- Fecha de Registro (auto)
- Estado Activo

### Equipo
- Cliente (FK)
- Código (único)
- Nombre
- Tipo (Máquina, Electrónico, Sistema, Vehículo, Otro)
- Marca
- Modelo
- Número de Serie (único)
- Fecha de Instalación
- Ubicación
- Ficha Técnica
- Estado Activo

### Técnico
- Usuario Django (OneToOne)
- RUT (único)
- Especialidad
- Teléfono
- Fecha de Contratación
- Estado Activo

### Plan de Mantención
- Equipo (FK)
- Nombre
- Descripción
- Frecuencia (Diaria, Semanal, Mensual, etc.)
- Duración Estimada (horas)
- Procedimiento
- Estado Activo

### Orden de Trabajo
- Equipo (FK)
- Técnico (FK, nullable)
- Plan de Mantención (FK, nullable)
- Código (único)
- Descripción
- Fecha de Solicitud (auto)
- Fecha Programada
- Fecha Inicio Real (nullable)
- Fecha Fin Real (nullable)
- Estado (Pendiente, En Proceso, Finalizada, Cancelada)
- Prioridad (Baja, Media, Alta, Urgente)
- Observaciones
- Costo Estimado
- Costo Real (nullable)

## Configuración de Desarrollo

### Variables de Entorno Recomendadas
```
DEBUG=True
SECRET_KEY=tu-clave-secreta
ALLOWED_HOSTS=127.0.0.1,localhost
```

### Estructura del Proyecto
```
Evaluacion_4-main/
├── config/              # Configuración principal del proyecto
│   ├── settings.py      # Configuración de Django
│   ├── urls.py          # URLs principales
│   ├── wsgi.py
│   └── asgi.py
├── api/                 # Aplicación principal
│   ├── models.py        # Modelos ORM (5 entidades)
│   ├── serializers.py   # Serializers para la API
│   ├── views.py         # ViewSets y lógica de negocio
│   ├── urls.py          # URLs de la API
│   ├── admin.py         # Configuración de admin
│   ├── migrations/      # Migraciones de base de datos
│   └── tests.py         # Tests unitarios
├── manage.py            # Utilidad de Django
├── requirements.txt     # Dependencias del proyecto
├── README.md            # Este archivo
└── db.sqlite3           # Base de datos (SQLite)
```

## Pruebas y Validación

Para verificar que todo está configurado correctamente:
```bash
python manage.py check
```

Para ejecutar los tests:
```bash
python manage.py test
```

## Próximas Mejoras
- [ ] Implementar más validaciones en serializers
- [ ] Agregar tests unitarios
- [ ] Documentación con Swagger/OpenAPI
- [ ] Logging y monitoreo
- [ ] Caché de resultados
- [ ] Rate limiting en endpoints

## Licencia
Proyecto académico - Sin licencia específica

## Autor
Desarrollado como evaluación de la asignatura Programación Backend (TI2041)
