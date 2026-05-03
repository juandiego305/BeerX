from rest_framework import permissions

class EsAdministrador(permissions.BasePermission):
    """
    Permiso que solo permite el acceso a usuarios con rol 'ADMIN'.
    """
    def has_permission(self, request, view):
        # 1. Verificamos que el usuario esté logueado
        if not request.user or not request.user.is_authenticated:
            return False
        
        # 2. Verificamos si su rol es 'ADMIN'
        # Nota: Usamos .upper() por si acaso se guardó en minúsculas
        return request.user.rol and request.user.rol.nombre.upper() == 'ADMIN'

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
            
        return request.user.rol and request.user.rol.nombre.upper() == 'ADMIN'