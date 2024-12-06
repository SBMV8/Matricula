from django import forms
from usuarios.models import Usuario

class RegistroUsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    rol = forms.ChoiceField(choices=[('estudiante', 'Estudiante'), ('docente', 'Docente')], label="Rol")
    # Campos adicionales para estudiantes administrativos y director
    codigo = forms.CharField(max_length=10, label="Código")
    nombres = forms.CharField(max_length=100, label="Nombres")
    apellidos = forms.CharField(max_length=100, label="Apellidos")
    plan_estudios = forms.CharField(max_length=4, required=False, label="Plan de estudios")
    telefono = forms.CharField(max_length=15, required=False, label="Teléfono")
    escuela = forms.CharField(max_length=100, required=False, label="Escuela")
    nivel = forms.IntegerField(required=False, label="Nivel")
    ciclo = forms.IntegerField(required=False, label="Ciclo")

    class Meta:
        model = Usuario
        fields = ['correo', 'password', 'rol']
        
    def clean(self):
        cleaned_data = super().clean()
        rol = cleaned_data.get("rol")
        # Si el rol es "estudiante", los campos de estudiante son requeridos
        if rol == 'estudiante':
            if cleaned_data.get("escuela"):
                self.add_error("escuela", "Este campo es requerido para estudiantes.")
            if not cleaned_data.get("plan_estudios"):
                self.add_error("plan_estudios", "Este campo es requerido para estudiantes.")
            if cleaned_data.get("nivel") is None:
                self.add_error("nivel", "Este campo es requerido para estudiantes.")
            if cleaned_data.get("ciclo") is None:
                self.add_error("ciclo", "Este campo es requerido para estudiantes.")
        elif rol=="docente":
            if not cleaned_data.get("escuela"):
                self.add_error("escuela", "Este campo es requerido para docente.")

        return cleaned_data