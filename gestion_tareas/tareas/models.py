from django.db import models

# Create your models here.
class Familia(models.Model):
  """Modelo para agrupar tareas por familias."""
  nombre = models.CharField(max_length=100, unique=True, verbose_name='Nombre de la familia')

  class Meta:
    """Creo esta clase para definir metadatos del modelo de tal manera que aparezca de manera más legible en el panel de administración."""
    verbose_name = 'Familia'
    verbose_name_plural = 'Familias'
    ordering = ['nombre'] # Ordena por orden alfabético cuando pida la lista de familias

  def __str__(self):
    """Define como se representa este objeto (Familia) en el panel de administración como texto."""
    return self.nombre
  
class Tarea(models.Model):
  """Modelo para crear tareas.
  Es la entidad principal que representa las actividades que se pueden realizar.
  """
  class Estado(models.TextChoices):
    """Estados de las tareas.
    El primer valor es lo que se guarda en la base de datos y el segundo es lo que se muestra en el panel de administración.
    """
    PENDIENTE = 'pendiente', 'Pendiente'
    EN_PROGRESO = 'en_progreso', 'En progreso'
    COMPLETADA = 'completada', 'Completada'

  familia = models.ForeignKey( # Relación con la entidad Familia (1 - N, es decir, una misma tarea puede pertenecer a muchas familias)
    Familia,
    on_delete=models.PROTECT, # Aunque no lo pide el enunciado me ha parecido pertinente hacer que no se puedan eliminar familias con tareas asociadas para no dejar tareas huerfanas
    related_name='tareas', # Permite hacer que se muestren las tareas de una familia en el panel de administración
    verbose_name='Familia' # Define el nombre de la familia en el panel de administración
  )

  titulo = models.CharField(max_length=200, verbose_name="Título") 
  descripcion = models.TextField(blank=True, verbose_name="Descripción") # blank permite que el campo no sea obligatorio
  estado = models.CharField(
    max_length=20, 
    choices=Estado.choices, # Obliga a elegir uno de los valores definidos en la clase Estado
    default=Estado.PENDIENTE, # Define el estado por defecto
    verbose_name="Estado"
  )
  fecha_creacion = models.DateTimeField(
    auto_now_add=True, # Django asigna la fecha y hora actual al crear el objeto
    verbose_name="Fecha de creación"
  )
  fecha_vencimiento = models.DateTimeField(
    null=True, # Permite valor null en la bbdd
    blank=True, # Permite valor null en el panel de administración
    verbose_name="Fecha de vencimiento"
  )

  class Meta:
    """Igual que con la clase anterior, esta clase define los metadatos de manera legible para el panel de administración."""
    verbose_name = 'Tarea'
    verbose_name_plural = 'Tareas'
    ordering = ['-fecha_vencimiento'] # Orden descendente por fecha de vencimiento

  def __str__(self):
    """Define como se representa este objeto (Tarea) en el panel de administración como texto."""
    return f"{self.titulo} ({self.get_estado_display()})" # Empleo el getter generado por Django para campos 'choices' para obtener el nombre del estado