from django import forms
from usuarios.models import Usuario
from django.core.exceptions import ValidationError

class RegistroUsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")

    # Campos adicionales para estudiantes y administrativos
    codigo = forms.CharField(max_length=10, label="Código")
    nombres = forms.CharField(max_length=100, label="Nombres")
    apellidos = forms.CharField(max_length=100, label="Apellidos")
    telefono = forms.CharField(max_length=15, required=False, label="Teléfono")
    # Solo para estudiantes
    escuela = forms.CharField(max_length=100, required=False, label="Escuela")
    plan_estudios = forms.CharField(max_length=4, required=False, label="Plan de estudios")
    nivel = forms.IntegerField(required=False, label="Nivel")
    ciclo = forms.IntegerField(required=False, label="Ciclo")

    class Meta:
        model = Usuario
        fields = ['correo', 'password', 'rol']

    def clean_correo(self):
        correo = self.cleaned_data.get("correo")
        if correo and not correo.endswith('@unfv.edu.pe'):
            raise ValidationError("El correo debe terminar en @unfv.edu.pe.")
        return correo

    def clean(self):
        cleaned_data = super().clean()
        rol = cleaned_data.get("rol")
        
        # Validaciones específicas para el rol 'estudiante'
        if rol == 'estudiante':
            if cleaned_data.get("escuela") is None:
                self.add_error("escuela", "Este campo es requerido para estudiantes.")
            if not cleaned_data.get("plan_estudios"):
                self.add_error("plan_estudios", "Este campo es requerido para estudiantes.")
            if cleaned_data.get("nivel") is None:
                self.add_error("nivel", "Este campo es requerido para estudiantes.")
            if cleaned_data.get("ciclo") is None:
                self.add_error("ciclo", "Este campo es requerido para estudiantes.")

        return cleaned_data
