from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoriaViewSet, ProductoViewSet, MovimientoViewSet, StockActualViewSet

router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet)
router.register(r'productos', ProductoViewSet)
router.register(r'movimientos', MovimientoViewSet)
router.register(r'dashboard/stock', StockActualViewSet, basename='dashboard-stock')

urlpatterns = [
    path('api/', include(router.urls)),
]