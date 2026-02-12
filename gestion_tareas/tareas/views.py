from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from dj_rest_auth.views import UserDetailsView, LogoutView
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status

from .models import Tarea, Familia
from .serializers import FamiliaSerializer, TareaSerializer
from .filters import TareaFilter
from .permissions import ReadOnlyForUsers


# ------------------------------------------------------------
# FAMILIAS
# ------------------------------------------------------------
class FamiliaViewSet(viewsets.ModelViewSet):
    """
    - Lectura: todos los usuarios autenticados.
    - Escritura: solo administradores.
    """
    permission_classes = [ReadOnlyForUsers]
    queryset = Familia.objects.all()
    serializer_class = FamiliaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre']
    ordering_fields = ['nombre']


# ------------------------------------------------------------
# TAREAS
# ------------------------------------------------------------
class TareaViewSet(viewsets.ModelViewSet):
    """
    - Lectura: todos los usuarios autenticados (ven TODAS las tareas).
    - Escritura: solo administradores.
    """
    permission_classes = [ReadOnlyForUsers]
    serializer_class = TareaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = TareaFilter
    search_fields = ['titulo', 'descripcion']
    ordering_fields = ['fecha_creacion', 'fecha_vencimiento', 'estado']

    def get_queryset(self):
        # ✅ TODOS ven TODAS las tareas
        return Tarea.objects.select_related('familia', 'usuario').all()

    def perform_create(self, serializer):
        # Asignar usuario autenticado (solo admin puede crear)
        serializer.save(usuario=self.request.user)


# ------------------------------------------------------------
# LOGOUT PERSONALIZADO (borra cookies JWT)
# ------------------------------------------------------------
class CustomLogoutView(LogoutView):
    def logout(self, request):
        response = Response(
            {"detail": "Sesión cerrada correctamente."},
            status=status.HTTP_200_OK,
        )
        # Eliminar cookies JWT
        response.delete_cookie(
            settings.JWT_AUTH_COOKIE,
            domain=settings.JWT_AUTH_COOKIE_DOMAIN,
            path='/',
            samesite=settings.JWT_AUTH_COOKIE_SAMESITE,
        )
        response.delete_cookie(
            settings.JWT_AUTH_REFRESH_COOKIE,
            domain=settings.JWT_AUTH_COOKIE_DOMAIN,
            path='/',
            samesite=settings.JWT_AUTH_COOKIE_SAMESITE,
        )
        # Eliminar cookies de sesión y CSRF
        response.delete_cookie('sessionid', domain=settings.SESSION_COOKIE_DOMAIN, path='/')
        response.delete_cookie('csrftoken', domain=settings.CSRF_COOKIE_DOMAIN, path='/')
        return response


# ------------------------------------------------------------
# DETALLE DE USUARIO
# ------------------------------------------------------------
class CustomUserDetailsView(UserDetailsView):
    permission_classes = [ReadOnlyForUsers]

    def get(self, request, *args, **kwargs):
        print("👤 Entrando a CustomUserDetailsView.get()")
        print(f"Usuario autenticado: {request.user}")
        return super().get(request, *args, **kwargs)