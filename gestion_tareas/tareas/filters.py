import django_filters
from .models import Tarea

class TareaFilter(django_filters.FilterSet):
    """
    Define cómo se pueden filtrar los datos de las Tareas cuando se hace una petición a la API. 
    Utiliza la librería django-filter para añadir lógica personalizada que no viene por defecto en Django.
    """
    # Filtro por estado (opciones exactas). Solo aceptará los valores predefinidos en el modelo Tarea (por ejemplo: 'Pendiente', 'En proceso', 'Completada')
    estado = django_filters.ChoiceFilter(choices=Tarea.Estado.choices)
    
    # Filtro por familia (por ID). Le indica a Django que entre a la entidad familia y filtre por ID mediante el doble guión bajo
    familia = django_filters.NumberFilter(field_name='familia__id')
    
    # Filtro por rango de fecha de vencimiento
    fecha_vencimiento_desde = django_filters.DateFilter(
        field_name='fecha_vencimiento', lookup_expr='gte' # Busca valores mayores o iguales
    )
    fecha_vencimiento_hasta = django_filters.DateFilter(
        field_name='fecha_vencimiento', lookup_expr='lte' # Busca valores menores o iguales
    )
    
    # Filtro por tareas vencidas (fecha_vencimiento < hoy)
    vencidas = django_filters.BooleanFilter( # Define un filtro booleano, retorna True o False
        method='filter_vencidas', # Emplea el método 'filter_vencidas'
        label='Solo vencidas' # Define el nombre que se muestra en el panel de administración
    )
    
    def filter_vencidas(self, queryset, name, value):
        from django.utils import timezone # necesario para saber la fecha actual
        hoy = timezone.now().date()
        if value: # si el usuario ha marcado el checkbox retorna las tareas vencidas
            return queryset.filter(fecha_vencimiento__lt=hoy)
        return queryset # retorna todas las tareas si el checkbox no ha sido marcado

    class Meta:
        """Indicamos que campos queremos que se muestren en el panel de administración"""
        model = Tarea # Establece sobre que tabla se aplicarán los filtros
        fields = ['estado', 'familia', 'fecha_vencimiento'] # Campos mostrados