from django import forms
from django.contrib.auth import get_user_model, password_validation

Usuario = get_user_model()


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
        help_texts = {
            'username': ''  # ← esto elimina el texto por defecto de Django
        }

    def __init__(self, *args, **kwargs):
        crear = kwargs.pop('crear', False)  # ← flag que pasamos desde la vista
        super().__init__(*args, **kwargs)
        if crear:
            self.fields['password'].required = True
            self.fields['password'].help_text = "La contraseña debe tener al menos 8 caracteres."
        else:
            self.fields['password'].required = False
            self.fields['password'].help_text = "Deja en blanco si no deseas cambiar la contraseña."

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

    def clean(self):
        cleaned_data = super().clean()
        rol = cleaned_data.get("rol")
        direccion = cleaned_data.get("direccion_inicial")

        # Validar que si el rol es ciudadano, la dirección sea obligatoria
        if rol == Usuario.Rol.CIUDADANO and not direccion:
            self.add_error("direccion_inicial", "La dirección es obligatoria para ciudadanos.")

        return cleaned_data
