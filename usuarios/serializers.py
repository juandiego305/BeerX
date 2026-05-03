from rest_framework import serializers
from .models import Usuario, Rol

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'rol']
        extra_kwargs = {
            'password': {'write_only': True} # La contraseña no se envía de vuelta por seguridad
        }

    def create(self, validated_data):
        # Extraemos la contraseña para manejarla por separado
        password = validated_data.pop('password')
        # Creamos el usuario sin la contraseña aún
        user = Usuario(**validated_data)
        # Encriptamos la contraseña con el método de Django
        user.set_password(password)
        user.save()
        return user