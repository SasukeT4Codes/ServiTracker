from django.db import models
from django.contrib.auth.models import AbstractUser

# -------------------
# Usuario personalizado
# -------------------
class Usuario(AbstractUser):
    class Rol(models.TextChoices):
        CIUDADANO = 'ciudadano', 'Ciudadano'
        TECNICO = 'tecnico', 'Técnico'
        ADMINISTRATIVO = 'administrativo', 'Administrativo'

    telefono = models.CharField(max_length=20, blank=True, null=True)
    rol = models.CharField(max_length=20, choices=Rol.choices, default=Rol.CIUDADANO)

    # Campos adicionales
    numero_documento = models.CharField(max_length=50, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    numero_cuenta = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Número de cuenta de servicio asignado por la empresa"
    )

    def __str__(self):
        return f"{self.username} ({self.rol})"


# -------------------
# Perfiles 1:1
# -------------------
class Ciudadano(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    telefono_alternativo = models.CharField(max_length=20, blank=True, null=True)

    # Datos adicionales
    tipo_documento = models.CharField(max_length=30, blank=True, null=True)
    numero_documento = models.CharField(max_length=50, blank=True, null=True)
    numero_cuenta = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Número de cuenta de servicio asignado por la empresa"
    )

    def __str__(self):
        return f"Ciudadano: {self.usuario.username}"


class Tecnico(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    especialidad = models.CharField(max_length=100, blank=True)
    zona_asignada = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Técnico: {self.usuario.username}"


class Administrativo(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    departamento = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Administrativo: {self.usuario.username}"
