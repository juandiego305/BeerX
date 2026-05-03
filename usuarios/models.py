import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

class Rol(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class Usuario(AbstractUser):
    # Usamos UUID por seguridad en vez de IDs secuenciales
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    
    # Llave foránea hacia el rol (ON DELETE RESTRICT para proteger la integridad)
    rol = models.ForeignKey(Rol, on_delete=models.RESTRICT, null=True, blank=True)

    # Configuración para que Django exija el email y lo use como principal
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email