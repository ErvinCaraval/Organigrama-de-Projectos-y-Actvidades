from rest_framework import serializers
from .models import Proyecto, Tarea 
from django.core.exceptions import ValidationError
from django.utils import timezone

class ProyectoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proyecto
        fields = '__all__'

    def validate(self, attrs):
        if attrs.get('fecha_inicio') and attrs.get('fecha_fin'):
            if attrs['fecha_fin'] < attrs['fecha_inicio']:
                raise serializers.ValidationError('La fecha de fin no puede ser anterior a la fecha de inicio del proyecto.')
        return attrs


class TareaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarea
        fields = '__all__'

    def validate(self, attrs):
        fecha_inicio_tarea = attrs.get('fecha_inicio')
        fecha_fin_tarea = attrs.get('fecha_fin')
        proyecto = attrs.get('proyecto')

        if fecha_inicio_tarea and fecha_fin_tarea:
            if fecha_fin_tarea < fecha_inicio_tarea:
                raise serializers.ValidationError('La fecha de fin no puede ser anterior a la fecha de inicio de la tarea.')

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

        return attrs

