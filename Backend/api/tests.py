from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Proyecto, Tarea
from rest_framework.test import APIClient
from rest_framework import status

class TestProyectoModel(TestCase):
    def setUp(self):
        self.proyecto = Proyecto.objects.create(nombre="Proyecto Test", descripcion="Descripción de prueba",
                                                fecha_inicio=timezone.now(), fecha_fin=None)

    def test_proyecto_creation(self):
        proyecto = Proyecto.objects.get(nombre="Proyecto Test")
        self.assertEqual(proyecto.nombre, "Proyecto Test")
        self.assertEqual(proyecto.descripcion, "Descripción de prueba")
        self.assertTrue(proyecto.fecha_inicio)
        self.assertIsNone(proyecto.fecha_fin)
        self.assertFalse(proyecto.terminado)

    def test_invalid_proyecto_dates(self):
        with self.assertRaises(ValidationError):
            Proyecto.objects.create(nombre="Proyecto Invalido", descripcion="Descripción de prueba",
                                    fecha_inicio=timezone.now(), fecha_fin=timezone.now()-timezone.timedelta(days=1))

    def test_clean_method(self):
        proyecto = Proyecto(nombre="Proyecto con Nombre Inválido-!@", descripcion="Descripción de prueba",
                            fecha_inicio=timezone.now(), fecha_fin=None)
        with self.assertRaises(ValidationError):
            proyecto.full_clean()

class TestTareaModel(TestCase):
    def setUp(self):
        self.proyecto = Proyecto.objects.create(nombre="Proyecto Test", descripcion="Descripción de prueba",
                                                fecha_inicio=timezone.now(), fecha_fin=None)
        self.tarea = Tarea.objects.create(proyecto=self.proyecto, nombre="Tarea Test",
                                          descripcion="Descripción de tarea de prueba",
                                          fecha_inicio=timezone.now(), fecha_fin=None)

    def test_tarea_creation(self):
        tarea = Tarea.objects.get(nombre="Tarea Test")
        self.assertEqual(tarea.nombre, "Tarea Test")
        self.assertEqual(tarea.descripcion, "Descripción de tarea de prueba")
        self.assertTrue(tarea.fecha_inicio)
        self.assertIsNone(tarea.fecha_fin)
        self.assertTrue(tarea.sin_terminar)
        self.assertFalse(tarea.terminado)

    def test_invalid_tarea_dates(self):
        with self.assertRaises(ValidationError):
            Tarea.objects.create(proyecto=self.proyecto, nombre="Tarea Inválida", descripcion="Descripción de tarea de prueba",
                                 fecha_inicio=timezone.now(), fecha_fin=timezone.now()-timezone.timedelta(days=1))

    def test_clean_method(self):
        tarea = Tarea(proyecto=self.proyecto, nombre="Tarea con Nombre Inválido-!@", descripcion="Descripción de tarea de prueba",
                      fecha_inicio=timezone.now(), fecha_fin=None)
        with self.assertRaises(ValidationError):
            tarea.full_clean()

class TestProyectoViewSet(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(username='admin', email='admin@example.com', password='adminpassword')
        self.client.force_authenticate(user=self.admin_user)
        self.proyecto = Proyecto.objects.create(nombre="Proyecto Test", descripcion="Descripción de prueba",
                                                fecha_inicio=timezone.now(), fecha_fin=None)
        self.url = reverse('proyecto-detail', kwargs={'pk': self.proyecto.pk})

    def test_get_proyecto_list(self):
        response = self.client.get(reverse('proyecto-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_proyecto(self):
        new_data = {
            'nombre': 'Proyecto Actualizado',
            'descripcion': 'Descripción actualizada',
            'start_date': timezone.now(),
            'end_date': timezone.now() + timezone.timedelta(days=1)
        }
        response = self.client.put(self.url, new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_proyecto = Proyecto.objects.get(pk=self.proyecto.pk)
        self.assertEqual(updated_proyecto.nombre, 'Proyecto Actualizado')
        self.assertEqual(updated_proyecto.descripcion, 'Descripción actualizada')

    def test_delete_proyecto(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Proyecto.DoesNotExist):
            Proyecto.objects.get(pk=self.proyecto.pk)

    # Añadir más pruebas según sea necesario para Tarea y otros endpoints de API

class TestTareaViewSet(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(username='admin', email='admin@example.com', password='adminpassword')
        self.client.force_authenticate(user=self.admin_user)
        self.proyecto = Proyecto.objects.create(nombre="Proyecto Test", descripcion="Descripción de prueba",
                                                fecha_inicio=timezone.now(), fecha_fin=None)
        self.tarea = Tarea.objects.create(proyecto=self.proyecto, nombre="Tarea Test",
                                          descripcion="Descripción de tarea de prueba",
                                          fecha_inicio=timezone.now(), fecha_fin=None)
        self.url = reverse('tarea-detail', kwargs={'pk': self.tarea.pk})

    def test_get_tarea_list(self):
        response = self.client.get(reverse('tarea-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_tarea(self):
        new_data = {
            'nombre': 'Tarea Actualizada',
            'descripcion': 'Descripción actualizada',
            'start_date': timezone.now(),
            'end_date': timezone.now() + timezone.timedelta(days=1)
        }
        response = self.client.put(self.url, new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_tarea = Tarea.objects.get(pk=self.tarea.pk)
        self.assertEqual(updated_tarea.nombre, 'Tarea Actualizada')
        self.assertEqual(updated_tarea.descripcion, 'Descripción actualizada')

    def test_delete_tarea(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Tarea.DoesNotExist):
            Tarea.objects.get(pk=self.tarea.pk)

    # Añadir más pruebas según sea necesario para otros endpoints de API


