from django.contrib import admin
from django.urls import path
from core import views  # Asegúrate de importar tus vistas

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),  # 🔹 Verifica que esta línea esté presente
]
