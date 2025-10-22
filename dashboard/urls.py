from django.urls import path
from . import views

urlpatterns = [
    path('ciudadano/', views.dashboard_ciudadano, name='dashboard_ciudadano'),
    path('tecnico/', views.dashboard_tecnico, name='dashboard_tecnico'),
    path('admin/', views.dashboard_admin, name='dashboard_admin'),
]
