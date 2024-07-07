from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Proyecto, Tarea
from .serializers import ProyectoSerializer, TareaSerializer
from django.core.exceptions import ValidationError
from django.db import transaction, IntegrityError
from django.db.models import F
import logging

logger = logging.getLogger(__name__)

class ProyectoViewSet(viewsets.ModelViewSet):
    queryset = Proyecto.objects.all()
    serializer_class = ProyectoSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        logger.info(f"Acceso al detalle del Proyecto {instance.nombre} mediante GET - ID: {instance.proyecto_id}")
        return super().retrieve(request, *args, **kwargs)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            logger.info(f"Proyecto creado correctamente - ID: {response.data.get('proyecto_id')}")
            return response
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        try:
            response = super().update(request, *args, **kwargs)
            logger.info(f"Proyecto actualizado correctamente - ID: {response.data.get('proyecto_id')}")
            return response
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            return Response({'error': 'Error de integridad al actualizar el proyecto.'}, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        try:
            proyecto_id = kwargs.get('pk')
            proyecto = Proyecto.objects.select_for_update().get(pk=proyecto_id)
            proyecto.delete()
            logger.info(f"Proyecto eliminado correctamente - ID: {proyecto_id}")
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Proyecto.DoesNotExist:
            return Response({'error': 'El proyecto especificado no existe.'}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError as e:
            return Response({'error': 'Error de integridad al eliminar el proyecto.'}, status=status.HTTP_400_BAD_REQUEST)

class TareaViewSet(viewsets.ModelViewSet):
    queryset = Tarea.objects.all()
    serializer_class = TareaSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        logger.info(f"Acceso al detalle de la Tarea {instance.nombre} en Proyecto {instance.proyecto.nombre} mediante GET - ID: {instance.tarea_id}")
        return super().retrieve(request, *args, **kwargs)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            logger.info(f"Tarea creada correctamente - ID: {response.data.get('tarea_id')}")
            return response
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        try:
            response = super().update(request, *args, **kwargs)
            logger.info(f"Tarea actualizada correctamente - ID: {response.data.get('tarea_id')}")
            return response
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            return Response({'error': 'Error de integridad al actualizar la tarea.'}, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        try:
            tarea_id = kwargs.get('pk')
            tarea = Tarea.objects.select_for_update().get(pk=tarea_id)
            tarea.delete()
            logger.info(f"Tarea eliminada correctamente - ID: {tarea_id}")
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Tarea.DoesNotExist:
            return Response({'error': 'La tarea especificada no existe.'}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError as e:
            return Response({'error': 'Error de integridad al eliminar la tarea.'}, status=status.HTTP_400_BAD_REQUEST)
