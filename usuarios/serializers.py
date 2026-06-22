from rest_framework import serializers
from .models import Usuario, Rol

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        # 1. Agregamos 'is_active' al final para que React pueda leer y cambiar el estado
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'rol', 'is_active']
        extra_kwargs = {
            # 2. Le agregamos 'required': False para poder hacer PATCH sin enviar contraseña obligatoria
            'password': {'write_only': True, 'required': False} 
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

    # 3. Agregamos el método update para manejar las ediciones desde el panel
    def update(self, instance, validated_data):
        # Extraemos la contraseña (si viene, bien; si no, queda como None)
        password = validated_data.pop('password', None)
        
        # Actualizamos todos los demás campos (nombre, email, rol, is_active, etc.)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            
        # Si el administrador escribió una nueva contraseña en React, la encriptamos
        if password:
            instance.set_password(password)
            
        instance.save()
        return instance