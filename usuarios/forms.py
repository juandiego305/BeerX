from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import Usuario


class UsuarioCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ('email', 'username', 'first_name', 'last_name', 'rol', 'is_active', 'is_staff')


class UsuarioChangeForm(UserChangeForm):
    class Meta:
        model = Usuario
        fields = ('email', 'username', 'first_name', 'last_name', 'rol', 'is_active', 'is_staff')