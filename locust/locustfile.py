import random
from locust import HttpUser, TaskSet, task, between
import re

class ProyectoTasks(TaskSet):

    @task(1)
    def create_proyecto(self):
        nombre = f"Proyecto {random.randint(1, 1000000)}"
        if re.match(r'^[\w\s]+$', nombre) and len(nombre.split()) <= 20:
            self.client.post("http://web:8000/api/v1/api/proyectos/", json={
                "nombre": nombre,
                "descripcion": "Descripción del proyecto de prueba",
                "fecha_inicio": "2023-01-01T00:00:00Z",
                "fecha_fin": "2023-12-31T23:59:59Z"
            })

    @task(3)
    def update_proyecto(self):
        proyectos = self.client.get("http://web:8000/api/v1/api/proyectos/").json()
        if proyectos:
            proyecto_id = random.choice(proyectos)["proyecto_id"]
            nombre = f"Proyecto Actualizado {random.randint(1, 1000000)}"
            if re.match(r'^[\w\s]+$', nombre) and len(nombre.split()) <= 20:
                self.client.put(f"http://web:8000/api/v1/api/proyectos/{proyecto_id}/", json={
                    "nombre": nombre,
                    "descripcion": "Descripción actualizada",
                    "fecha_inicio": "2023-01-01T00:00:00Z",
                    "fecha_fin": "2023-12-31T23:59:59Z",
                    "terminado": False
                })

    @task(6)
    def delete_proyecto(self):
        proyectos = self.client.get("http://web:8000/api/v1/api/proyectos/").json()
        if proyectos:
            proyecto_id = random.choice(proyectos)["proyecto_id"]
            self.client.delete(f"http://web:8000/api/v1/api/proyectos/{proyecto_id}/")

class TareaTasks(TaskSet):

    @task(2)
    def create_tarea(self):
        proyectos = self.client.get("http://web:8000/api/v1/api/proyectos/").json()
        if proyectos:
            proyecto_id = random.choice(proyectos)["proyecto_id"]
            nombre = f"Tarea {random.randint(1, 1000000)}"
            if re.match(r'^[\w\s]+$', nombre) and len(nombre.split()) <= 20:
                self.client.post("http://web:8000/api/v1/api/tareas/", json={
                    "proyecto": proyecto_id,
                    "nombre": nombre,
                    "descripcion": "Descripción de la tarea de prueba",
                    "fecha_inicio": "2023-01-01T00:00:00Z",
                    "fecha_fin": "2023-12-31T23:59:59Z",
                    "sin_terminar": True,
                    "terminado": False
                })

    @task(4)
    def update_tarea(self):
        tareas = self.client.get("http://web:8000/api/v1/api/tareas/").json()
        if tareas:
            tarea_id = random.choice(tareas)["tarea_id"]
            nombre = f"Tarea Actualizada {random.randint(1, 1000000)}"
            if re.match(r'^[\w\s]+$', nombre) and len(nombre.split()) <= 20:
                self.client.put(f"http://web:8000/api/v1/api/tareas/{tarea_id}/", json={
                    "nombre": nombre,
                    "descripcion": "Descripción actualizada",
                    "fecha_inicio": "2023-01-01T00:00:00Z",
                    "fecha_fin": "2023-12-31T23:59:59Z",
                    "sin_terminar": False,
                    "terminado": True
                })

    @task(5)
    def delete_tarea(self):
        tareas = self.client.get("http://web:8000/api/v1/api/tareas/").json()
        if tareas:
            tarea_id = random.choice(tareas)["tarea_id"]
            self.client.delete(f"http://web:8000/api/v1/api/tareas/{tarea_id}/")

class ProjectManagementUser(HttpUser):
    tasks = {ProyectoTasks: 1, TareaTasks: 1}  # Ejecutar ambas clases de manera concurrente
    wait_time = between(1, 5)  # Tiempo de espera entre tareas
