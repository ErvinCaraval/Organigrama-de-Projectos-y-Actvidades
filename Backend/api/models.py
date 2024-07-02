from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

class Proyecto(models.Model):
    proyecto_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    fecha_inicio = models.DateTimeField(default=timezone.now)
    fecha_fin = models.DateTimeField(blank=True, null=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    terminado = models.BooleanField(default=False)  # Campo para marcar el proyecto como terminado

    def clean(self):
        if self.fecha_inicio and self.fecha_fin:
            if self.fecha_fin < self.fecha_inicio:
                raise ValidationError('La fecha de fin no puede ser anterior a la fecha de inicio del proyecto.')

    def __str__(self):
        return self.nombre

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

    def clean(self):
        # Verificar que la fecha de inicio de la tarea está dentro del rango del proyecto
        if self.proyecto:
            if self.fecha_inicio < self.proyecto.fecha_inicio:
                raise ValidationError('La fecha de inicio de la tarea no puede ser anterior a la fecha de inicio del proyecto.')

            if self.fecha_fin and (self.fecha_fin < self.fecha_inicio or (self.proyecto.fecha_fin and self.fecha_fin > self.proyecto.fecha_fin)):
                raise ValidationError('La fecha de fin de la tarea debe estar dentro del rango de fechas del proyecto.')

    def __str__(self):
        return self.nombre

@receiver(post_save, sender=Tarea)
@receiver(post_delete, sender=Tarea)
def actualizar_estado_proyecto(sender, instance, **kwargs):
    proyecto = instance.proyecto
    if proyecto:
        tareas_sin_terminar = proyecto.tareas.filter(sin_terminar=True).exists()
        if not tareas_sin_terminar:
            proyecto.terminado = True
            proyecto.save()

class Registro(models.Model):
    registro_id = models.AutoField(primary_key=True)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, blank=True, null=True, related_name='registros')
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE, blank=True, null=True, related_name='registros')
    accion = models.CharField(max_length=50)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    usuario_id = models.ForeignKey('auth.User', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        if self.proyecto:
            return f"Registro de Proyecto: {self.proyecto.nombre} - Acción: {self.accion}"
        elif self.tarea:
            return f"Registro de Tarea: {self.tarea.nombre} - Acción: {self.accion}"
        return f"Registro - Acción: {self.accion}"

class RegistroAuditoria(models.Model):
    auditoria_id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    accion = models.CharField(max_length=50)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, blank=True, null=True, related_name='auditorias')
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE, blank=True, null=True, related_name='auditorias')

    def __str__(self):
        related_object = self.proyecto if self.proyecto else self.tarea
        return f"Auditoría - Usuario: {self.usuario.username} - Acción: {self.accion} - Objeto: {related_object}"

    def clean(self):
        # Asegurar que al menos uno de proyecto o tarea esté presente
        if not self.proyecto and not self.tarea:
            raise ValidationError('Debe especificar un proyecto o una tarea para la auditoría.')
