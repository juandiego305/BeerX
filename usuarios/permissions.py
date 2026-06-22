from rest_framework import permissions


def _es_admin(usuario):
    return bool(usuario and usuario.is_authenticated and usuario.rol and usuario.rol.nombre.upper() == 'ADMIN')


def _es_empleado(usuario):
    return bool(usuario and usuario.is_authenticated and usuario.rol and usuario.rol.nombre.upper() == 'EMPLEADO')


class EsAdministrador(permissions.BasePermission):
    """
    Permiso que solo permite el acceso a usuarios con rol 'ADMIN'.
    """
    def has_permission(self, request, view):
        return _es_admin(request.user)

class EsAdminOReadOnly(permissions.BasePermission):
    """
    Si es una petición de lectura (GET), cualquier logueado entra.
    Si es escritura (POST, PUT, DELETE), solo el ADMIN.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.method in permissions.SAFE_METHODS: # GET, HEAD, OPTIONS
            return True

        return _es_admin(request.user)


class EsAdminOEmpleadoVentas(permissions.BasePermission):
    """
    Permite acceso a ADMIN o EMPLEADO.
    Se usa para registrar ventas desde movimientos de inventario.
    """

    def has_permission(self, request, view):
        return _es_admin(request.user) or _es_empleado(request.user)