from rest_framework import serializers
from .models import Tarea, Familia
from django.utils import timezone

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

  # ? DRF busca automáticamente métodos que empiecen con la palabra validate_ seguidos del nombre de un campo para aplicar reglas de negocio
  def validate_fecha_vencimiento(self, value):
        """Evita que un usuario cree una tarea que ya expiró"""
        if value and value < timezone.now().date():
            raise serializers.ValidationError("La fecha de vencimiento no puede ser anterior a hoy.")
        return value

  def validate_estado(self, value):
      """Convierte las opciones del modelo en un diccionario para verificar rápidamente si el estado enviado existe."""
      if value not in dict(Tarea.Estado.choices): # Lo hace 'choices' por defecto pero es una capa de seguridad extra
          raise serializers.ValidationError("Estado no válido.")
      return value
  
class FamiliaSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Familia."""
    class Meta:
        model = Familia
        fields = ['id', 'nombre']