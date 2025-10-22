from django.urls import path
from . import views

urlpatterns = [
    # Gestión de usuarios (solo admin)
    path('admin/usuarios/', views.admin_gestion_usuarios, name='admin_gestion_usuarios'),
    path('admin/usuarios/crear/', views.admin_crear_usuario, name='admin_crear_usuario'),
    path('admin/usuarios/<int:usuario_id>/editar/', views.admin_editar_usuario, name='admin_editar_usuario'),
    path('admin/usuarios/<int:usuario_id>/eliminar/', views.admin_eliminar_usuario, name='admin_eliminar_usuario'),
]
