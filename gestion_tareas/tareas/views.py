from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Tarea, Familia
from .serializers import FamiliaSerializer
from .serializers import TareaSerializer
from .filters import TareaFilter

# Create your views here.
class FamiliaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para realizar CRUD completo de Familias.
    """
    queryset = Familia.objects.all()
    serializer_class = FamiliaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre']
    ordering_fields = ['nombre']

class TareaViewSet(viewsets.ModelViewSet):
  """
  ViewSet para CRUD de Tareas.
  Django rest framework genera automáticamente el CRUD al heredar de ModelViewSet.
  Permite filtrar, buscar y ordenar las tareas.
  """
  queryset = Tarea.objects.select_related('familia').all() # Indica de donde se van a obtener los datos. Emplear `select_related` trae la información de las familias relacionadas a dicha tarea, dicho de otra manera, es como un JOIN de SQL
  serializer_class = TareaSerializer # Especifica el serializador que convierta los objetos en JSON
  filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter] # Indica los filtros que se van a usar: DjangoFilterBackend (filtro por campos exactos), SearchFilter (barra de búsqueda) y OrderingFilter (permite elegir el orden de resultado de las tareas)
  filterset_class = TareaFilter # uso de'.filters.py', ver bibliografia sobre filtros personalizados.
  search_fields = ['titulo', 'descripcion'] # Indica los campos por los cuales se puede buscar '?search=...'
  ordering_fields = ['fecha_creacion', 'fecha_vencimiento', 'estado'] # Establece los campos por los cuales se puede ordenar la lista '?ordering=...'
