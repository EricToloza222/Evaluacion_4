from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Cliente

class ClienteTests(TestCase):
    def setUp(self):
        # Configuración inicial para cada prueba
        self.client = APIClient()
        
        # Crear un usuario administrador para las pruebas de escritura
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        
        # Datos de prueba
        self.cliente_data = {
            'rut': '11111111-1',
            'razon_social': 'Empresa Test',
            'giro': 'Pruebas',
            'direccion': 'Calle Falsa 123',
            'telefono': '999999999',
            'email': 'test@empresa.com'
        }
        self.cliente = Cliente.objects.create(**self.cliente_data)

    def test_listar_clientes_publico(self):
        """Cualquier usuario (anonimo) debería poder ver la lista de clientes."""
        response = self.client.get('/api/clientes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_crear_cliente_sin_auth(self):
        # Un usuario NO autenticado NO debería poder crear clientes
        nuevo_cliente = {
            'rut': '22222222-2',
            'razon_social': 'Empresa Intrusa',
            'giro': 'Hacking',
            'direccion': 'Dark Web',
            'telefono': '000000000',
            'email': 'hacker@mail.com'
        }
        response = self.client.get('/api/clientes/', nuevo_cliente, format='json')
        # Debería recibir un 401 Unauthorized o 403 Forbidden, no un 201 Created
        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)

    def test_crear_cliente_con_auth(self):
        # Nos autenticamos forzadamente
        self.client.force_authenticate(user=self.user)
        
        nuevo_cliente = {
            'rut': '33333333-3',
            'razon_social': 'Empresa Nueva',
            'giro': 'Desarrollo',
            'direccion': 'Av Siempre Viva',
            'telefono': '123456789',
            'email': 'nueva@empresa.com'
        }
        response = self.client.post('/api/clientes/', nuevo_cliente, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cliente.objects.count(), 2)