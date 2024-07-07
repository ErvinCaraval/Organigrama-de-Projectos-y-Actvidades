# Importaciones necesarias
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import re
import logging

# Configuración del logger
logger = logging.getLogger(__name__)

# Modelo Proyecto
class Proyecto(models.Model):
    proyecto_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    fecha_inicio = models.DateTimeField(default=timezone.now)
    fecha_fin = models.DateTimeField(blank=True, null=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    terminado = models.BooleanField(default=False)

    def clean(self):
        if self.fecha_inicio > timezone.now():
            raise ValidationError('La fecha de inicio no puede estar en el futuro.')

        if self.fecha_inicio and self.fecha_fin:
            if self.fecha_fin < self.fecha_inicio:
                raise ValidationError('La fecha de fin no puede ser anterior a la fecha de inicio del proyecto.')

        if not re.match(r'^[\w\s]+$', self.nombre):
            raise ValidationError('El nombre del proyecto solo debe contener caracteres alfanuméricos y espacios.')
        if len(self.nombre.split()) > 20:
            raise ValidationError('El nombre del proyecto no puede exceder 20 palabras.')

        if self.descripcion:
            if len(self.descripcion) > 250:
                raise ValidationError('La descripción no puede exceder 250 caracteres.')
            if not re.match(r'^[\w\s.,!?\-\'"]*$', self.descripcion):
                raise ValidationError('La descripción contiene caracteres no permitidos.')

    def __str__(self):
        return self.nombre

# Señales para el modelo Proyecto
@receiver(post_save, sender=Proyecto)
def log_proyecto_actions(sender, instance, created, **kwargs):
    action = "CREATED" if created else "UPDATED"
    logger.info(f"Proyecto {instance.nombre} {action} - ID: {instance.proyecto_id}")

@receiver(post_delete, sender=Proyecto)
def log_proyecto_delete(sender, instance, **kwargs):
    logger.info(f"Proyecto {instance.nombre} DELETED - ID: {instance.proyecto_id}")

# Modelo Tarea
class Tarea(models.Model):
    tarea_id = models.AutoField(primary_key=True)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='tareas')
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    fecha_inicio = models.DateTimeField(default=timezone.now)
    fecha_fin = models.DateTimeField(blank=True, null=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    sin_terminar = models.BooleanField(default=True)
    terminado = models.BooleanField(default=False)

    class Meta:
        unique_together = ('proyecto', 'nombre')

    def clean(self):
        if self.sin_terminar and self.terminado:
            raise ValidationError('Una tarea no puede estar marcada como sin terminar y terminada al mismo tiempo.')

        if not self.sin_terminar and not self.terminado:
            raise ValidationError('Una tarea debe estar marcada como sin terminar o terminada.')

        if self.fecha_inicio > timezone.now():
            raise ValidationError('La fecha de inicio no puede estar en el futuro.')

        if self.proyecto:
            if self.fecha_inicio < self.proyecto.fecha_inicio:
                raise ValidationError('La fecha de inicio de la tarea no puede ser anterior a la fecha de inicio del proyecto.')
            if self.fecha_fin and (self.fecha_fin < self.fecha_inicio or (self.proyecto.fecha_fin and self.fecha_fin > self.proyecto.fecha_fin)):
                raise ValidationError('La fecha de fin de la tarea debe estar dentro del rango de fechas del proyecto.')

        if not re.match(r'^[\w\s]+$', self.nombre):
            raise ValidationError('El nombre de la tarea solo debe contener caracteres alfanuméricos y espacios.')
        if len(self.nombre.split()) > 20:
            raise ValidationError('El nombre de la tarea no puede exceder 20 palabras.')

        if self.descripcion:
            if len(self.descripcion) > 250:
                raise ValidationError('La descripción no puede exceder 250 caracteres.')
            if not re.match(r'^[\w\s.,!?\-\'"]*$', self.descripcion):
                raise ValidationError('La descripción contiene caracteres no permitidos.')

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        super(Tarea, self).save(*args, **kwargs)
        self.actualizar_estado_proyecto()

    def actualizar_estado_proyecto(self):
        proyecto = self.proyecto
        if proyecto:
            tareas_sin_terminar = proyecto.tareas.filter(sin_terminar=True)
            if not tareas_sin_terminar.exists():
                proyecto.terminado = True
                proyecto.save()
            else:
                proyecto.terminado = False
                proyecto.save()

# Señales para el modelo Tarea
@receiver(post_save, sender=Tarea)
def log_tarea_actions(sender, instance, created, **kwargs):
    action = "CREATED" if created else "UPDATED"
    logger.info(f"Tarea {instance.nombre} {action} en Proyecto {instance.proyecto.nombre} - ID: {instance.tarea_id}")

@receiver(post_delete, sender=Tarea)
def log_tarea_delete(sender, instance, **kwargs):
    logger.info(f"Tarea {instance.nombre} DELETED en Proyecto {instance.proyecto.nombre} - ID: {instance.tarea_id}")
