from django.urls import path
from .views import RegistrarUsuarioView, ListaUsuariosView, ModificarUsuarioView

urlpatterns = [
    # Ruta POST: http://127.0.0.1:8000/usuarios/register/ (Crear)
    path('register/', RegistrarUsuarioView.as_view(), name='auth_register'),
    
    # Ruta GET: http://127.0.0.1:8000/usuarios/api/ (Listar)
    path('api/', ListaUsuariosView.as_view(), name='listar_usuarios'),
    
    # Ruta PATCH/PUT/GET: http://127.0.0.1:8000/usuarios/api/1/ (Modificar o desactivar)
    path('api/<int:pk>/', ModificarUsuarioView.as_view(), name='modificar_usuario'),
]