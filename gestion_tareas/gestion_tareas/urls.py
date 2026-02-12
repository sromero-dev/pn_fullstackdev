from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tareas.views import TareaViewSet, FamiliaViewSet
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from tareas.views import CustomUserDetailsView
from tareas.views import CustomLogoutView
from django.conf import settings

router = DefaultRouter()
router.register(r'tareas', TareaViewSet, basename='tarea')
router.register(r'familias', FamiliaViewSet, basename='familia')

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = 'http://localhost:5173/auth/callback'
    client_class = OAuth2Client

    def post(self, request, *args, **kwargs):
        # 1. Ejecutar el flujo completo de la vista padre
        response = super().post(request, *args, **kwargs)

        # 2. Obtener tokens desde self (asignados por super().post)
        access_token = getattr(self, 'access_token', None)
        refresh_token = getattr(self, 'refresh_token', None)

        # 3. Fallback: si no están en self, extraer de response.data
        if access_token is None and isinstance(response.data, dict):
            access_token = response.data.get('access') or response.data.get('access_token')
        if refresh_token is None and isinstance(response.data, dict):
            refresh_token = response.data.get('refresh') or response.data.get('refresh_token')

        # 4. Establecer cookies JWT manualmente
        if access_token:
            response.set_cookie(
                key=settings.JWT_AUTH_COOKIE,
                value=access_token,
                domain=settings.JWT_AUTH_COOKIE_DOMAIN,
                secure=settings.JWT_AUTH_COOKIE_SECURE,
                httponly=True,
                samesite=settings.JWT_AUTH_COOKIE_SAMESITE,
            )
        if refresh_token:
            response.set_cookie(
                key=settings.JWT_AUTH_REFRESH_COOKIE,
                value=refresh_token,
                domain=settings.JWT_AUTH_COOKIE_DOMAIN,
                secure=settings.JWT_AUTH_COOKIE_SECURE,
                httponly=True,
                samesite=settings.JWT_AUTH_COOKIE_SAMESITE,
            )

        return response
    
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),

    path('api/auth/social/google/callback/', GoogleLogin.as_view(), name='google_callback'),

    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),

    path('api/auth/user/', CustomUserDetailsView.as_view(), name='custom_user_details'),
    path('api/auth/logout/', CustomLogoutView.as_view(), name='rest_logout'),
    path('api/auth/', include('dj_rest_auth.urls')),
]