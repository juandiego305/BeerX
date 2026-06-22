from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action

# Importamos nuestros modelos y serializadores
from .models import Categoria, Producto, MovimientosInventario, StockActual
from .serializers import (
    CategoriaSerializer, 
    ProductoSerializer, 
    MovimientoSerializer, 
    StockActualSerializer
)

# Importamos los permisos personalizados que creamos
from usuarios.permissions import EsAdministrador, EsAdminOReadOnly, EsAdminOEmpleadoVentas


class CategoriaViewSet(viewsets.ModelViewSet):
    """
    Gestión de categorías. 
    Seguridad: Solo el ADMIN puede crear, editar o eliminar.
    """
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [EsAdministrador]


class ProductoViewSet(viewsets.ModelViewSet):
    """
    Gestión de productos con Borrado Lógico (Soft Delete).
    Seguridad: Cualquiera puede ver (GET), solo ADMIN puede modificar (POST, PUT, DELETE).
    """
    # Usamos .all() para que el Admin pueda ver tanto los activos como inactivos en Postman/Frontend
    queryset = Producto.objects.all().order_by('id')
    serializer_class = ProductoSerializer
    permission_classes = [EsAdminOReadOnly]

    # 1. SOBREESCRIBIMOS EL MÉTODO DELETE (Para apagar, no borrar)
    def destroy(self, request, *args, **kwargs):
        producto = self.get_object()
        producto.is_active = False
        producto.save()
        
        return Response(
            {"mensaje": f"El producto '{producto.nombre}' ha sido desactivado (No eliminado)."},
            status=status.HTTP_200_OK
        )

    # 2. CREAMOS UNA RUTA NUEVA PARA REACTIVAR
    @action(detail=True, methods=['post'])
    def activar(self, request, pk=None):
        producto = self.get_object()
        producto.is_active = True
        producto.save()
        
        return Response(
            {"mensaje": f"El producto '{producto.nombre}' ha sido activado nuevamente."},
            status=status.HTTP_200_OK
        )


class MovimientoViewSet(viewsets.ModelViewSet):
    """
    Gestión de entradas y salidas de inventario.
    Seguridad: Cualquier usuario logueado (Admin o Empleado) puede registrar movimientos.
    """
    queryset = MovimientosInventario.objects.all().order_by('-fecha_movimiento')
    serializer_class = MovimientoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action == 'create':
            return [EsAdminOEmpleadoVentas()]

        return [EsAdministrador()]

    # Aseguramos que el guardado se ejecute correctamente. 
    # La validación de stock y asignación de usuario están en el Serializador.
    def perform_create(self, serializer):
        serializer.save()


class StockActualViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Dashboard de métricas. 
    Seguridad: Solo lectura para cualquier usuario logueado.
    Nota: Se alimenta de la vista 'vw_stock_actual' en Neon.
    """
    queryset = StockActual.objects.all()
    serializer_class = StockActualSerializer
    permission_classes = [permissions.IsAuthenticated]