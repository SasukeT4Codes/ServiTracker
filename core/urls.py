from django.urls import path
from .views import index, saludo

urlpatterns = [
    path('', index, name='index'),
    path('saludo/', saludo, name='saludo'),
]
