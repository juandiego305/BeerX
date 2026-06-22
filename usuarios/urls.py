from django.urls import path
from .views import RegistrarUsuarioView, ListaUsuariosView, ModificarUsuarioView

urlpatterns = [
    # Ruta POST (Crear)
    path('register/', RegistrarUsuarioView.as_view(), name='auth_register'),
    
    # Ruta GET (Listar)
    path('api/', ListaUsuariosView.as_view(), name='listar_usuarios'),
    
    # ¡AQUÍ ESTÁ EL CAMBIO! Cambiamos <int:pk> por <str:pk>
    path('api/<str:pk>/', ModificarUsuarioView.as_view(), name='modificar_usuario'),
]