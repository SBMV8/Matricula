from django.contrib import admin
from .models import Curso, CursoAprobado, Matricula

# Configuración para el modelo Curso
@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('codigo_curso', 'nombre', 'creditos', 'nivel', 'ciclo', 'pre_requisito','vacantes')
    search_fields = ('codigo_curso', 'nombre')
    list_filter = ('nivel', 'ciclo')
    ordering = ('nivel', 'ciclo', 'codigo_curso')

# Configuración para el modelo CursoAprobado
@admin.register(CursoAprobado)
class CursoAprobadoAdmin(admin.ModelAdmin):
    list_display = ('estudiante', 'curso', 'fecha_aprobacion', 'nota', 'aprobado')
    search_fields = ('estudiante__nombres', 'estudiante__apellidos', 'curso__nombre')
    list_filter = ('aprobado', 'fecha_aprobacion')
    ordering = ('fecha_aprobacion', 'estudiante', 'curso')
    autocomplete_fields = ['estudiante', 'curso']  # Autocompletar para buscar estudiantes y cursos más fácilmente

@admin.register(Matricula)
class MatriculaAdmin(admin.ModelAdmin):
    list_display = ('mostrar_codigo', 'escuela', 'plan', 'celular',
                    'num_recibo_primero', 'num_recibo_segundo', 
                    'monto_recibo_primero', 'monto_recibo_segundo',
                    'mostrar_cursos1', 'mostrar_cursos2', 
                    'fecha_matricula', 'estado')  # Añadimos 'estado'
    
    list_editable = ('estado',)  # Permite editar el estado directamente en la lista
    filter_horizontal = ('semestre1', 'semestre2',)

    def mostrar_codigo(self, obj):
        return obj.codigo.codigo_estudiante  # Mostrar solo el código del estudiante
    
    mostrar_codigo.short_description = 'Código Estudiante'

    def mostrar_cursos1(self, obj):
        return ", ".join([curso.nombre for curso in obj.semestre1.all()])  # Cambia 'asignatura' si es necesario

    def mostrar_cursos2(self, obj):
        return ", ".join([curso.nombre for curso in obj.semestre2.all()])

    mostrar_cursos1.short_description = 'Semestre 1' 
    mostrar_cursos2.short_description = 'Semestre 2'




