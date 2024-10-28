from django import forms
from .models import Curso, CursoAprobado,Matricula,DocumentosMatricula


# Formulario para el modelo Curso
class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['codigo_curso', 'nombre', 'creditos', 'nivel', 'ciclo', 'pre_requisito']

# Formulario para el modelo CursoAprobado
class CursoAprobadoForm(forms.ModelForm):
    class Meta:
        model = CursoAprobado
        fields = ['estudiante', 'curso', 'fecha_aprobacion', 'nota']

class MatriculaForm(forms.ModelForm):
    cursos = forms.ModelMultipleChoiceField(
        queryset=Curso.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    class Meta:
        model = Matricula
        fields = ['escuela', 'plan', 'celular',
                  'num_recibo_primero', 'num_recibo_segundo', 
                  'monto_recibo_primero', 'monto_recibo_segundo',
                  'semestre1','semestre2']
class DocumentosMatriculaForm(forms.ModelForm):
    class Meta:
        model = DocumentosMatricula
        fields = ['recibo_pago_1','recibo_pago_2', 'boleta_notas','matricula']
        widgets = {
            'recibo_pago_1': forms.FileInput(attrs={'class': 'form-control'}),
            'recibo_pago_2': forms.FileInput(attrs={'class': 'form-control'}),
            'boleta_notas': forms.FileInput(attrs={'class': 'form-control'}),
        }