from django.contrib import admin
from .models import Proyecto, Tarea, Registro, RegistroAuditoria

admin.site.register(Proyecto)
admin.site.register(Tarea)
admin.site.register(Registro)
admin.site.register(RegistroAuditoria)
