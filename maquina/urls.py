from django.contrib import admin
from django.urls import path
from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>¡Bienvenido a mi proyecto Django!</h1>")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # 🔹 Agregamos esta línea
]
