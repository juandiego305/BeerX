from rest_framework import generics, permissions
from .models import Usuario
from .serializers import UsuarioSerializer
from .permissions import EsAdministrador

# ==========================================
# 1. CREAR USUARIO (POST) - El que ya tenías
# ==========================================
class RegistrarUsuarioView(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [EsAdministrador]

# ==========================================
# 2. LISTAR USUARIOS (GET) - Para la tabla de React
# ==========================================
class ListaUsuariosView(generics.ListAPIView):
    # Usamos order_by('-id') para que los más nuevos salgan arriba
    queryset = Usuario.objects.all().order_by('-id')
    serializer_class = UsuarioSerializer
    permission_classes = [EsAdministrador]

# ==========================================
# 3. EDITAR/DESACTIVAR USUARIO (PATCH / PUT)
# ==========================================
class ModificarUsuarioView(generics.RetrieveUpdateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [EsAdministrador]