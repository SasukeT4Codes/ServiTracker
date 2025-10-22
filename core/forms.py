from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation
from .models import Queja, ComentarioQueja, Ciudadano

Usuario = get_user_model()


# -------------------
# Formularios de Queja
# -------------------
class QuejaForm(forms.ModelForm):
    class Meta:
        model = Queja
        fields = ['direccion', 'tipo_falla', 'descripcion']
        widgets = {
            'direccion': forms.Select(attrs={'class': 'form-select'}),
            'tipo_falla': forms.Select(attrs={'class': 'form-select'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
        labels = {
            'direccion': 'Dirección',
            'tipo_falla': 'Tipo de falla',
            'descripcion': 'Descripción',
        }

    def clean_descripcion(self):
        desc = self.cleaned_data.get('descripcion', '')
        if len(desc) < 10:
            raise forms.ValidationError("La descripción debe tener al menos 10 caracteres.")
        return desc


class QuejaFormAdmin(forms.ModelForm):
    class Meta:
        model = Queja
        fields = ['ciudadano', 'direccion', 'tipo_falla', 'descripcion']
        widgets = {
            'ciudadano': forms.Select(attrs={'class': 'form-select'}),
            'direccion': forms.Select(attrs={'class': 'form-select'}),
            'tipo_falla': forms.Select(attrs={'class': 'form-select'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
        labels = {
            'ciudadano': 'Ciudadano',
            'direccion': 'Dirección',
            'tipo_falla': 'Tipo de falla',
            'descripcion': 'Descripción',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ciudadano'].queryset = Ciudadano.objects.select_related('usuario').order_by('usuario__username')


# -------------------
# Comentarios
# -------------------
class ComentarioForm(forms.ModelForm):
    class Meta:
        model = ComentarioQueja
        fields = ['mensaje']
        widgets = {
            'mensaje': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Escribe tu comentario...'}),
        }
        labels = {
            'mensaje': 'Comentario',
        }

    def clean_mensaje(self):
        msg = self.cleaned_data.get('mensaje', '')
        if not msg.strip():
            raise forms.ValidationError("El mensaje no puede estar vacío.")
        return msg


# -------------------
# Cambiar estado de la queja
# -------------------
class CambiarEstadoForm(forms.ModelForm):
    class Meta:
        model = Queja
        fields = ['estado']
        widgets = {
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'estado': 'Estado',
        }


# -------------------
# Formulario de Usuario
# -------------------
class UsuarioForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False,
        help_text="Deja en blanco si no deseas cambiar la contraseña."
    )

    # Campo adicional para dirección inicial
    direccion_inicial = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Dirección inicial"
    )

    class Meta:
        model = Usuario
        fields = [
            'username', 'email', 'rol', 'is_active', 'telefono',
            'numero_documento', 'fecha_nacimiento', 'numero_cuenta', 'password'
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'rol': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_documento': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'numero_cuenta': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'username': 'Usuario',
            'email': 'Correo electrónico',
            'rol': 'Rol',
            'is_active': 'Activo',
            'telefono': 'Teléfono',
            'numero_documento': 'Número de documento',
            'fecha_nacimiento': 'Fecha de nacimiento',
            'numero_cuenta': 'Número de cuenta de servicio',
        }

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        if pwd:
            password_validation.validate_password(pwd, self.instance)
        return pwd

    def save(self, commit=True):
        user = super().save(commit=False)
        pwd = self.cleaned_data.get('password')
        if pwd:
            user.set_password(pwd)
        if commit:
            user.save()
        return user
