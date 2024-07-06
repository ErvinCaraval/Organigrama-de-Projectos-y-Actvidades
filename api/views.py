from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Proyecto, Tarea
from .serializers import ProyectoSerializer, TareaSerializer
from django.core.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)

class ProyectoViewSet(viewsets.ModelViewSet):
    queryset = Proyecto.objects.all()
    serializer_class = ProyectoSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        logger.info(f"Acceso al detalle del Proyecto {instance.nombre} mediante GET - ID: {instance.proyecto_id}")
        return super().retrieve(request, *args, **kwargs)

class TareaViewSet(viewsets.ModelViewSet):
    queryset = Tarea.objects.all()
    serializer_class = TareaSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        logger.info(f"Acceso al detalle de la Tarea {instance.nombre} en Proyecto {instance.proyecto.nombre} mediante GET - ID: {instance.tarea_id}")
        return super().retrieve(request, *args, **kwargs)

    def perform_create(self, serializer):
        try:
            serializer.save()
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        try:
            serializer.save()
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
