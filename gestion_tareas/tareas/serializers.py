from rest_framework import serializers
from .models import Tarea

class TareaSerializer(serializers.ModelSerializer):
  """Serializer para el modelo Tarea."""
  # Muestra el nombre de la familia en el panel de administración en lugar de SOLO el ID de familia (esto es puramente opcional, no lo pone en el enunciado)
  familia_nombre = serializers.CharField(source='familia.nombre', read_only=True)

  class Meta:
    """Maneja el comportamiento del serializer."""
    model = Tarea # Indica que debe trabajar con el modelo Tarea
    fields = [ # Indica los campos que se muestran en la API
      'id', 'familia', 'familia_nombre', 
      'titulo', 'descripcion', 'estado', 
      'fecha_creacion', 'fecha_vencimiento'
    ]
    read_only_fields = ['fecha_creacion'] # Define campos que no se pueden modificar