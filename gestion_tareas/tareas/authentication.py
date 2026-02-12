from dj_rest_auth.jwt_auth import JWTCookieAuthentication
from django.conf import settings
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed

class DebugJWTCookieAuthentication(JWTCookieAuthentication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.jwt_auth_cookie = settings.JWT_AUTH_COOKIE

    def authenticate(self, request):
        print("\n========== DEBUG JWT COOKIE AUTH ==========")
        print(f"JWT_AUTH_COOKIE en settings: '{settings.JWT_AUTH_COOKIE}'")
        print(f"JWT_AUTH_COOKIE en self: '{self.jwt_auth_cookie}'")
        print(f"Cookies en request: {list(request.COOKIES.keys())}")
        token_cookie = request.COOKIES.get(self.jwt_auth_cookie)
        print(f"Token desde cookie (request.COOKIES): {token_cookie[:20] if token_cookie else 'None'}...")

        # --- Código IDÉNTICO al de JWTCookieAuthentication.authenticate ---
        if self.jwt_auth_cookie in request.COOKIES:
            print("✅ Cookie encontrada en request.COOKIES, autenticando...")
            token = request.COOKIES[self.jwt_auth_cookie]
            try:
                validated_token = self.get_validated_token(token)
                print("✅ get_validated_token OK")
                user = self.get_user(validated_token)
                print(f"✅ Usuario autenticado: {user} (ID: {user.id})")
                print("========== FIN DEBUG ==========\n")
                return (user, validated_token)
            except InvalidToken as e:
                print(f"❌ InvalidToken: {e}")
            except AuthenticationFailed as e:
                print(f"❌ AuthenticationFailed: {e}")
            except Exception as e:
                print(f"❌ Otra excepción: {e}")
        else:
            print("❌ Cookie NO encontrada en request.COOKIES (self.jwt_auth_cookie no está)")

        # Fallback al método padre (cabecera Authorization)
        print("⚠️  Fallback a super().authenticate (cabecera Authorization)")
        result = super().authenticate(request)
        print(f"Resultado del padre: {result}")
        print("========== FIN DEBUG ==========\n")
        return result