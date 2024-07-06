from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
import re
import logging

logger = logging.getLogger(__name__)

class Proyecto(models.Model):
    proyecto_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    fecha_inicio = models.DateTimeField(default=timezone.now)
    fecha_fin = models.DateTimeField(blank=True, null=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    terminado = models.BooleanField(default=False)  # Campo para marcar el proyecto como terminado

    def clean(self):
        # Validar que la fecha de inicio no esté en el futuro
        if self.fecha_inicio > timezone.now():
            raise ValidationError('La fecha de inicio no puede estar en el futuro.')

        # Validar que la fecha de fin no sea anterior a la fecha de inicio
        if self.fecha_inicio and self.fecha_fin:
            if self.fecha_fin < self.fecha_inicio:
                raise ValidationError('La fecha de fin no puede ser anterior a la fecha de inicio del proyecto.')

        # Validar que el nombre solo contenga caracteres alfanuméricos y espacios, y no exceda 20 palabras
        if not re.match(r'^[\w\s]+$', self.nombre):
            raise ValidationError('El nombre del proyecto solo debe contener caracteres alfanuméricos y espacios.')
        if len(self.nombre.split()) > 20:
            raise ValidationError('El nombre del proyecto no puede exceder 20 palabras.')

        # Validar que la descripción no exceda 250 caracteres y no contenga caracteres inseguros
        if self.descripcion:
            if len(self.descripcion) > 250:
                raise ValidationError('La descripción no puede exceder 250 caracteres.')
            if not re.match(r'^[\w\s.,!?\-\'"]*$', self.descripcion):
                raise ValidationError('La descripción contiene caracteres no permitidos.')

    def __str__(self):
        return self.nombre

@receiver(pre_save, sender=Proyecto)
def log_proyecto_get(sender, instance, **kwargs):
    logger.info(f"GET request for Proyecto {instance.nombre} - ID: {instance.proyecto_id}")

@receiver(post_save, sender=Proyecto)
def log_proyecto_actions(sender, instance, created, **kwargs):
    action = "CREATED" if created else "UPDATED"
    logger.info(f"Proyecto {instance.nombre} {action} - ID: {instance.proyecto_id}")

@receiver(post_delete, sender=Proyecto)
def log_proyecto_delete(sender, instance, **kwargs):
    logger.info(f"Proyecto {instance.nombre} DELETED - ID: {instance.proyecto_id}")    

class Tarea(models.Model):
    tarea_id = models.AutoField(primary_key=True)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='tareas')
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    fecha_inicio = models.DateTimeField(default=timezone.now)
    fecha_fin = models.DateTimeField(blank=True, null=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    sin_terminar = models.BooleanField(default=True)  # Campo para tareas no terminadas
    terminado = models.BooleanField(default=False)     # Campo para tareas terminadas

    class Meta:
        unique_together = ('proyecto', 'nombre')

    def clean(self):
        # Validar que una tarea no puede estar marcada como sin terminar y terminada al mismo tiempo
        if self.sin_terminar and self.terminado:
            raise ValidationError('Una tarea no puede estar marcada como sin terminar y terminada al mismo tiempo.')

        # Validar que una tarea debe estar marcada como sin terminar o terminada
        if not self.sin_terminar and not self.terminado:
            raise ValidationError('Una tarea debe estar marcada como sin terminar o terminada.')

        # Validar que la fecha de inicio no esté en el futuro
        if self.fecha_inicio > timezone.now():
            raise ValidationError('La fecha de inicio no puede estar en el futuro.')

        # Verificar que la fecha de inicio de la tarea está dentro del rango del proyecto
        if self.proyecto:
            if self.fecha_inicio < self.proyecto.fecha_inicio:
                raise ValidationError('La fecha de inicio de la tarea no puede ser anterior a la fecha de inicio del proyecto.')
            if self.fecha_fin and (self.fecha_fin < self.fecha_inicio or (self.proyecto.fecha_fin and self.fecha_fin > self.proyecto.fecha_fin)):
                raise ValidationError('La fecha de fin de la tarea debe estar dentro del rango de fechas del proyecto.')

        # Validar que el nombre solo contenga caracteres alfanuméricos y espacios, y no exceda 20 palabras
        if not re.match(r'^[\w\s]+$', self.nombre):
            raise ValidationError('El nombre de la tarea solo debe contener caracteres alfanuméricos y espacios.')
        if len(self.nombre.split()) > 20:
            raise ValidationError('El nombre de la tarea no puede exceder 20 palabras.')

        # Validar que la descripción no exceda 250 caracteres y no contenga caracteres inseguros
        if self.descripcion:
            if len(self.descripcion) > 250:
                raise ValidationError('La descripción no puede exceder 250 caracteres.')
            if not re.match(r'^[\w\s.,!?\-\'"]*$', self.descripcion):
                raise ValidationError('La descripción contiene caracteres no permitidos.')

    def __str__(self):
        return self.nombre

@receiver(pre_save, sender=Tarea)
def log_tarea_get(sender, instance, **kwargs):
    logger.info(f"GET request for Tarea {instance.nombre} in Proyecto {instance.proyecto.nombre} - ID: {instance.tarea_id}")

@receiver(post_save, sender=Tarea)
def log_tarea_actions(sender, instance, created, **kwargs):
    action = "CREATED" if created else "UPDATED"
    logger.info(f"Tarea {instance.nombre} {action} en Proyecto {instance.proyecto.nombre} - ID: {instance.tarea_id}")

@receiver(post_delete, sender=Tarea)
def log_tarea_delete(sender, instance, **kwargs):
    logger.info(f"Tarea {instance.nombre} DELETED en Proyecto {instance.proyecto.nombre} - ID: {instance.tarea_id}")
