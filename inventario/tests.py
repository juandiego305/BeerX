from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import patch

from django.test import TestCase
from rest_framework.test import APIRequestFactory

from inventario.serializers import MovimientoSerializer
from inventario.views import ProductoViewSet, StockActualViewSet
from usuarios.models import Rol, Usuario
from usuarios.permissions import EsAdminOReadOnly


class PermisosEmpleadoInventarioTests(TestCase):
	def setUp(self):
		self.factory = APIRequestFactory()
		self.rol_admin = Rol.objects.create(nombre='ADMIN', descripcion='Administrador')
		self.rol_empleado = Rol.objects.create(nombre='EMPLEADO', descripcion='Empleado')

		self.admin = Usuario.objects.create_user(
			username='admin',
			email='admin@beerx.com',
			password='pass12345',
			first_name='Admin',
			last_name='User',
			rol=self.rol_admin,
		)
		self.empleado = Usuario.objects.create_user(
			username='empleado',
			email='empleado@beerx.com',
			password='pass12345',
			first_name='Empleado',
			last_name='User',
			rol=self.rol_empleado,
		)

	def test_empleado_no_puede_ver_stock_actual(self):
		request = self.factory.get('/inventario/api/dashboard/stock/')
		request.user = self.empleado

		permisos = StockActualViewSet().get_permissions()
		self.assertFalse(permisos[0].has_permission(request, StockActualViewSet()))

	def test_empleado_no_puede_crear_productos(self):
		request = self.factory.post('/inventario/api/productos/', {})
		request.user = self.empleado

		permisos = EsAdminOReadOnly()
		self.assertFalse(permisos.has_permission(request, ProductoViewSet()))

	def test_empleado_solo_puede_registrar_salidas(self):
		serializer = MovimientoSerializer(
			context={'request': SimpleNamespace(user=self.empleado)},
			data={
				'producto': 1,
				'tipo_movimiento': 'ENTRADA',
				'cantidad': Decimal('1.00'),
				'observaciones': 'Prueba',
			},
		)

		with patch('inventario.serializers.StockActual.objects.filter') as mock_filter:
			mock_filter.return_value.first.return_value = None
			self.assertFalse(serializer.is_valid())
			self.assertIn('tipo_movimiento', serializer.errors)

	def test_empleado_puede_registrar_salida(self):
		serializer = MovimientoSerializer(
			context={'request': SimpleNamespace(user=self.empleado)},
			data={
				'producto': 1,
				'tipo_movimiento': 'SALIDA',
				'cantidad': Decimal('1.00'),
				'observaciones': 'Venta',
			},
		)

		with patch('inventario.serializers.StockActual.objects.filter') as mock_filter:
			mock_filter.return_value.first.return_value = SimpleNamespace(stock_total=Decimal('10.00'))
			self.assertTrue(serializer.is_valid(), serializer.errors)
