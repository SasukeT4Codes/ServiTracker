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


# -------------------
# Direcciones de ciudadanos
# -------------------
class Ubicacion(models.Model):
    ciudadano = models.ForeignKey(Ciudadano, on_delete=models.CASCADE, related_name="direcciones")
    barrio = models.CharField(max_length=100, blank=True)
    direccion = models.CharField(max_length=255)
    referencia = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.direccion} ({self.ciudadano.usuario.username})"


# -------------------
# Tablas auxiliares
# -------------------
class TipoFalla(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre


class EstadoQueja(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre


# -------------------
# Queja principal
# -------------------
class Queja(models.Model):
    ciudadano = models.ForeignKey(Ciudadano, on_delete=models.CASCADE)
    direccion = models.ForeignKey(Ubicacion, on_delete=models.CASCADE, related_name="quejas")
    tecnico = models.ForeignKey(Tecnico, on_delete=models.SET_NULL, null=True, blank=True)
    administrativo = models.ForeignKey(Administrativo, on_delete=models.SET_NULL, null=True, blank=True)
    tipo_falla = models.ForeignKey(TipoFalla, on_delete=models.CASCADE)
    estado = models.ForeignKey(EstadoQueja, on_delete=models.CASCADE)
    descripcion = models.TextField()
    fecha_reporte = models.DateTimeField(auto_now_add=True)
    fecha_resolucion = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Queja #{self.id} - {self.ciudadano.usuario.username}"


# -------------------
# Comentarios de la queja
# -------------------
class ComentarioQueja(models.Model):
    queja = models.ForeignKey(Queja, on_delete=models.CASCADE, related_name="comentarios")
    autor = models.CharField(max_length=100)
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario en Queja #{self.queja.id} por {self.autor}"
