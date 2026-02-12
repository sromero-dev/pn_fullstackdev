from django.core.management.base import BaseCommand
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
from decouple import config

class Command(BaseCommand):
    help = 'Crea la aplicación social de Google para OAuth usando variables de entorno'

    def handle(self, *args, **options):
        # Asegurar que existe el sitio con SITE_ID 
        site_id = 1
        site, created = Site.objects.get_or_create(
            id=site_id,
            defaults={
                'domain': 'localhost:8000',
                'name': 'localhost'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Sitio con id {site_id} creado correctamente'))
        else:
            self.stdout.write(f'Sitio con id {site_id} ya existe')

        # Leer credenciales desde .env 
        client_id = config('CLIENT_ID_KEY', default='')
        secret = config('SECRET_KEY', default='')

        if not client_id or not secret:
            self.stdout.write(self.style.ERROR(
                '❌ Las variables CLIENT_ID_KEY y SECRET_KEY no fueron encontradas en el archivo .env'
            ))
            return

        if not client_id or not secret:
            self.stdout.write(self.style.ERROR(
                '❌ Las variables CLIENT_ID_KEY y SECRET_KEY no están definidas en el archivo .env'
            ))
            return

        # Crear o actualizar la SocialApp
        app, created = SocialApp.objects.get_or_create(
            provider='google',
            name='Google Login',
            defaults={
                'client_id': client_id,
                'secret': secret,
            }
        )

        if created:
            app.sites.add(site)
            self.stdout.write(self.style.SUCCESS('✅ SocialApp creada correctamente'))
        else:
            # Actualizar credenciales y asegurar sitio asociado
            app.client_id = client_id
            app.secret = secret
            app.save()
            app.sites.add(site)
            self.stdout.write(self.style.SUCCESS('🔄 SocialApp actualizada con nuevas credenciales'))