from django import forms
from .models import Queja, ComentarioQueja, Ubicacion
from usuarios.models import Ciudadano, Tecnico, Administrativo, Usuario

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

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Si el usuario es ciudadano, limitar direcciones a las suyas
        if user and hasattr(user, 'ciudadano'):
            self.fields['direccion'].queryset = user.ciudadano.direcciones.all()

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
        # Ordenar ciudadanos por username
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
