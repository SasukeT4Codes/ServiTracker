from django.urls import path
from . import views

urlpatterns = [
    path('crear/', views.crear_queja, name='crear_queja'),
    path('empleados/', views.panel_empleados, name='panel_empleados'),
    path('cambiar-estado/<int:queja_id>/', views.cambiar_estado, name='cambiar_estado'),
    path('comentario/<int:queja_id>/', views.agregar_comentario, name='agregar_comentario'),

    # Admin PQR
    path('admin/quejas/', views.admin_panel_quejas, name='admin_panel_quejas'),
    path('admin/quejas/<int:queja_id>/asignar/', views.admin_asignar_tecnico, name='admin_asignar_tecnico'),
    path('admin/quejas/<int:queja_id>/editar/', views.admin_editar_queja, name='admin_editar_queja'),
    path('admin/quejas/<int:queja_id>/eliminar/', views.admin_eliminar_queja, name='admin_eliminar_queja'),
    path('admin/reportes/', views.admin_reportes, name='admin_reportes'),
]
