from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from datetime import date
from tareas.models import Familia, Tarea

class TareaAPITestCase(APITestCase):
    """
    Esta clase es la que contiene las pruebas unitarias (tarea completamente opcional).

    Notas para mi mismo generadas por IA:
      El Router genera automáticamente un mapa de nombres de rutas para que no tengas que escribirlas a mano. La estructura que sigue es:

      Para la lista (GET/POST): [basename]-list

      Para el detalle (GET/PUT/DELETE): [basename]-detail

      ¿Por qué reverse en lugar de la URL escrita?
      En los tests usamos reverse('tarea-list') por una razón de mantenimiento:

      Si mañana decides cambiar la URL de api/tareas/ a api/mis-tareas/, solo tendrías que cambiarlo en el archivo urls.py.

      Como tus tests usan reverse, ellos buscarán automáticamente la nueva URL usando el "apodo" (tarea-list) y no tendrás que romperte la cabeza cambiando la URL en 50 tests distintos.
      En tu test, reverse('tarea-list') le pregunta a Django: "Oye, ¿cuál es la URL de la lista del recurso que apodamos 'tarea'?". Django mira tu router, ve que está bajo api/tareas/ y te devuelve el string /api/tareas/.
    """

    def setUp(self):
        """ 
        Creo una familia y una tarea de ejemplo para tener algo con lo que probar.
        """
        self.familia = Familia.objects.create(nombre="Trabajo")
        self.tarea = Tarea.objects.create(
            familia=self.familia,
            titulo="Tarea inicial",
            descripcion="Descripción",
            estado=Tarea.Estado.PENDIENTE,
            fecha_vencimiento=date(2026, 12, 31)
        )
        # * Se guardan las rutas (URLs) para no tener que escribirlas a mano cada vez de manera que se vuelva reutilizable
        self.tarea_url = reverse('tarea-list')  # La lista general
        self.tarea_detail_url = reverse('tarea-detail', args=[self.tarea.id]) # Una tarea específica

    def test_listar_tareas(self):
        """ Se comprueba si se devuelve una lista de tareas """
        response = self.client.get(self.tarea_url)
        # Espero un código 200 (todo OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Compruebo que al menos llegue la tarea que creamos en el setUp
        results = response.data['results'] if 'results' in response.data else response.data
        self.assertEqual(len(results), 1)

    def test_crear_tarea_valida(self):
        """ Creacion de una tarea con datos validos """
        data = {
            "familia": self.familia.id,
            "titulo": "Nueva tarea",
            "descripcion": "Contenido",
            "estado": "pendiente",
            "fecha_vencimiento": "2026-06-01"
        }
        response = self.client.post(self.tarea_url, data, format='json')
        # Si se crea, Django debe devolver un 201 (Creado)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Ahora hay 2 tareas en la base de datos
        self.assertEqual(Tarea.objects.count(), 2)

    def test_crear_tarea_sin_titulo(self):
        """ Comprueba si se crean tareas sin titulo, no debería permitirse """
        data = {
            "familia": self.familia.id,
            "titulo": "   ", # Título vacío
            "estado": "pendiente"
        }
        response = self.client.post(self.tarea_url, data, format='json')
        # Se espera un error 400 (Error del cliente) porque el título es obligatorio
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('titulo', response.data)

    def test_crear_tarea_fecha_vencimiento_pasada(self):
        """ Comprueba validator del serializer funciona correctamente """
        data = {
            "familia": self.familia.id,
            "titulo": "Tarea vieja",
            "fecha_vencimiento": "2020-01-01" # Fecha del pasado
        }
        response = self.client.post(self.tarea_url, data, format='json')
        # Error 400 porque el serializador no debería dejar pasar fechas pasadas
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_actualizar_tarea(self):
        """ Comprueba si se puede modificar el titulo y el estado de una tarea existente"""
        data = {
            "familia": self.familia.id,
            "titulo": "Título actualizado",
            "estado": "en_progreso"
        }
        response = self.client.put(self.tarea_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Refrescamos la tarea desde la base de datos para ver si de verdad cambió
        self.tarea.refresh_from_db()
        self.assertEqual(self.tarea.titulo, "Título actualizado")

    def test_eliminar_tarea(self):
        """ Comprueba la eliminación de una tarea """
        response = self.client.delete(self.tarea_detail_url)
        # Se espera el código 204 
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Tarea.objects.count(), 0)

    def test_filtro_por_estado(self):
        """ Compruebo que el filtro por estado funciona correctamente """
        # Creo una tarea completada
        Tarea.objects.create(familia=self.familia, titulo="Ya la hice", estado=Tarea.Estado.COMPLETADA)
        
        # Hago el filtro
        response = self.client.get(self.tarea_url, {'estado': 'pendiente'})
        results = response.data['results'] if 'results' in response.data else response.data
        
        # Debería encontrar solo la que acabo de crear, ninguna más
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['estado'], 'pendiente')

    def test_filtro_vencidas(self):
        """ Comprueba el filtro de tareas vencidas / caducadas """
        # Creo una tarea que venció hace años
        Tarea.objects.create(familia=self.familia, titulo="Tarea vieja", fecha_vencimiento=date(2020, 1, 1))
        
        # Pido dichas tareas
        response = self.client.get(self.tarea_url, {'vencidas': 'true'})
        results = response.data['results'] if 'results' in response.data else response.data # Empleo operadores ternarios para mayor claridad
        
        # Debería encontrar solo la que acabo de crear
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['titulo'], "Tarea vencida")