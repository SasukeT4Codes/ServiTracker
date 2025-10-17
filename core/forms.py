from django import forms
from .models import Queja, ComentarioQueja

class QuejaForm(forms.ModelForm):
    class Meta:
        model = Queja
        fields = ['ubicacion', 'tipo_falla', 'descripcion']

    def clean_descripcion(self):
        desc = self.cleaned_data['descripcion']
        if len(desc) < 10:
            raise forms.ValidationError("La descripción debe tener al menos 10 caracteres.")
        return desc


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = ComentarioQueja
        fields = ['mensaje']


class CambiarEstadoForm(forms.ModelForm):
    class Meta:
        model = Queja
        fields = ['estado']
