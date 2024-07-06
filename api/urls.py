# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from django.contrib import admin
from rest_framework.documentation import include_docs_urls

router = DefaultRouter()
router.register(r'proyectos', views.ProyectoViewSet)
router.register(r'tareas', views.TareaViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('docs/',include_docs_urls(title="Final API") )
]
