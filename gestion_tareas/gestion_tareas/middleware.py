import logging

logger = logging.getLogger(__name__)

class LogCookiesMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log de todas las cookies recibidas
        logger.info(f"Cookies recibidas: {request.COOKIES}")
        print("🔥 COOKIES EN REQUEST:", request.COOKIES)  # También imprime en consola
        response = self.get_response(request)
        return response