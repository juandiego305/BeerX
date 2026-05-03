from rest_framework import generics, permissions
from .models import Usuario
from .serializers import UsuarioSerializer

class RegistrarUsuarioView(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    # Por ahora lo dejamos público para que puedas probar, 
    # luego lo bloquearemos para que solo el ADMIN pueda registrar.
    permission_classes = [permissions.AllowAny]