from rest_framework import serializers, exceptions
from .models import Proyecto, Tarea
from django.db import transaction, IntegrityError
import re

class ProyectoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proyecto
        fields = '__all__'

    def validate(self, attrs):
        nombre = attrs.get('nombre')
        descripcion = attrs.get('descripcion')
        fecha_inicio = attrs.get('fecha_inicio')
        fecha_fin = attrs.get('fecha_fin')

        # Validación de fecha de inicio y fin
        if fecha_inicio and fecha_fin:
            if fecha_fin < fecha_inicio:
                raise serializers.ValidationError('La fecha de fin no puede ser anterior a la fecha de inicio del proyecto.')

        # Validación de nombre
        if nombre:
            if not re.match(r'^[\w\s]+$', nombre):
                raise serializers.ValidationError('El nombre del proyecto solo debe contener caracteres alfanuméricos y espacios.')
            if len(nombre.split()) > 20:
                raise serializers.ValidationError('El nombre del proyecto no puede exceder 20 palabras.')

        # Validación de descripción
        if descripcion:
            if len(descripcion) > 250:
                raise serializers.ValidationError('La descripción no puede exceder 250 caracteres.')
            if not re.match(r'^[\w\s.,!?\-\'"]*$', descripcion):
                raise serializers.ValidationError('La descripción contiene caracteres no permitidos.')

        return attrs

    def create(self, validated_data):
        try:
            with transaction.atomic():
                return super().create(validated_data)
        except IntegrityError:
            raise exceptions.ValidationError('Ha ocurrido un error al crear el proyecto.')

    def update(self, instance, validated_data):
        try:
            with transaction.atomic():
                return super().update(instance, validated_data)
        except IntegrityError:
            raise exceptions.ValidationError('Ha ocurrido un error al actualizar el proyecto.')

class TareaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarea
        fields = '__all__'

    def validate(self, attrs):
        nombre = attrs.get('nombre')
        descripcion = attrs.get('descripcion')
        fecha_inicio_tarea = attrs.get('fecha_inicio')
        fecha_fin_tarea = attrs.get('fecha_fin')
        proyecto = attrs.get('proyecto')
        sin_terminar = attrs.get('sin_terminar')
        terminado = attrs.get('terminado')

        # Validación de estado de tarea
        if sin_terminar and terminado:
            raise serializers.ValidationError('Una tarea no puede estar marcada como sin terminar y terminada al mismo tiempo.')
        if not sin_terminar and not terminado:
            raise serializers.ValidationError('Una tarea debe estar marcada como sin terminar o terminada.')

        # Validación de fecha de inicio y fin de la tarea
        if fecha_inicio_tarea and fecha_fin_tarea:
            if fecha_fin_tarea < fecha_inicio_tarea:
                raise serializers.ValidationError('La fecha de fin no puede ser anterior a la fecha de inicio de la tarea.')

        # Validación de fechas respecto al proyecto asociado
        if proyecto:
            fecha_inicio_proyecto = proyecto.fecha_inicio
            fecha_fin_proyecto = proyecto.fecha_fin

            if fecha_inicio_tarea:
                if fecha_inicio_tarea < fecha_inicio_proyecto:
                    raise serializers.ValidationError('La fecha de inicio de la tarea no puede ser anterior a la fecha de inicio del proyecto.')
                if fecha_fin_proyecto and fecha_inicio_tarea > fecha_fin_proyecto:
                    raise serializers.ValidationError('La fecha de inicio de la tarea no puede ser posterior a la fecha de fin del proyecto.')

            if fecha_fin_tarea:
                if fecha_fin_tarea < fecha_inicio_proyecto:
                    raise serializers.ValidationError('La fecha de fin de la tarea no puede ser anterior a la fecha de inicio del proyecto.')
                if fecha_fin_proyecto and fecha_fin_tarea > fecha_fin_proyecto:
                    raise serializers.ValidationError('La fecha de fin de la tarea no puede ser posterior a la fecha de fin del proyecto.')

        # Validación de nombre
        if nombre:
            if not re.match(r'^[\w\s]+$', nombre):
                raise serializers.ValidationError('El nombre de la tarea solo debe contener caracteres alfanuméricos y espacios.')
            if len(nombre.split()) > 20:
                raise serializers.ValidationError('El nombre de la tarea no puede exceder 20 palabras.')

        # Validación de descripción
        if descripcion:
            if len(descripcion) > 250:
                raise serializers.ValidationError('La descripción no puede exceder 250 caracteres.')
            if not re.match(r'^[\w\s.,!?\-\'"]*$', descripcion):
                raise serializers.ValidationError('La descripción contiene caracteres no permitidos.')

        return attrs

    def create(self, validated_data):
        try:
            with transaction.atomic():
                return super().create(validated_data)
        except IntegrityError:
            raise exceptions.ValidationError('Ha ocurrido un error al crear la tarea.')

    def update(self, instance, validated_data):
        try:
            with transaction.atomic():
                return super().update(instance, validated_data)
        except IntegrityError:
            raise exceptions.ValidationError('Ha ocurrido un error al actualizar la tarea.')
