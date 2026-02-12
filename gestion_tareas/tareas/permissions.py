from rest_framework import permissions

class EsAdmin(permissions.BasePermission):
    """Acceso total solo a administradores (para acciones de escritura)."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.perfil.rol == 'admin'


class ReadOnlyForUsers(permissions.BasePermission):
    """
    - Lectura (GET, HEAD, OPTIONS): cualquier usuario autenticado.
    - Escritura (POST, PUT, PATCH, DELETE): solo administradores.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.perfil.rol == 'admin'