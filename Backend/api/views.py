from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Proyecto, Tarea, Registro, RegistroAuditoria
from .serializers import ProyectoSerializer, TareaSerializer, RegistroSerializer, RegistroAuditoriaSerializer
from django.core.exceptions import ValidationError

class ProyectoViewSet(viewsets.ModelViewSet):
    queryset = Proyecto.objects.all()
    serializer_class = ProyectoSerializer

class TareaViewSet(viewsets.ModelViewSet):
    queryset = Tarea.objects.all()
    serializer_class = TareaSerializer

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

class RegistroViewSet(viewsets.ModelViewSet):
    queryset = Registro.objects.all()
    serializer_class = RegistroSerializer

class RegistroAuditoriaViewSet(viewsets.ModelViewSet):
    queryset = RegistroAuditoria.objects.all()
    serializer_class = RegistroAuditoriaSerializer
