from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Campos adicionales', {
            'fields': ('rol', 'telefono', 'numero_documento', 'fecha_nacimiento', 'numero_cuenta'),
        }),
    )
