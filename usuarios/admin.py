from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ngettext

from .forms import UsuarioChangeForm, UsuarioCreationForm
from .models import Rol, Usuario


@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
	list_display = ('nombre', 'descripcion')
	search_fields = ('nombre',)


@admin.register(Usuario)
class UsuarioAdmin(BaseUserAdmin):
	form = UsuarioChangeForm
	add_form = UsuarioCreationForm
	actions = ['desactivar_usuarios', 'activar_usuarios']

	list_display = ('email', 'username', 'first_name', 'last_name', 'rol', 'is_staff', 'is_active')
	list_filter = ('is_staff', 'is_superuser', 'is_active', 'rol')
	search_fields = ('email', 'username', 'first_name', 'last_name')
	ordering = ('email',)

	fieldsets = (
		(None, {'fields': ('email', 'username', 'password')}),
		('Información personal', {'fields': ('first_name', 'last_name', 'rol')}),
		('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
		('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
	)

	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('email', 'username', 'first_name', 'last_name', 'rol', 'is_active', 'is_staff', 'password1', 'password2'),
		}),
	)

	filter_horizontal = ('groups', 'user_permissions')

	@admin.action(description='Desactivar usuarios seleccionados')
	def desactivar_usuarios(self, request, queryset):
		updated = queryset.update(is_active=False)
		self.message_user(
			request,
			ngettext(
				'%d usuario fue desactivado.',
				'%d usuarios fueron desactivados.',
				updated,
			) % updated,
		)

	@admin.action(description='Activar usuarios seleccionados')
	def activar_usuarios(self, request, queryset):
		updated = queryset.update(is_active=True)
		self.message_user(
			request,
			ngettext(
				'%d usuario fue activado.',
				'%d usuarios fueron activados.',
				updated,
			) % updated,
		)
