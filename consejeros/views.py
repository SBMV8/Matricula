from django.shortcuts import render, redirect,get_object_or_404
from django.core.paginator import Paginator
from estudiantes.models import Curso
from usuarios.models import Estudiante, Administrativo, Usuario
from estudiantes.models import Matricula, DocumentosMatricula
from django.contrib import messages
# Create your views here.

def consejero_index(request):
    return render(request, 'consejeros/index.html')

def logout_view(request):
    # Eliminar el código de estudiante de la sesión
    if 'codigo_consejero' in request.session:
        del request.session['codigo_codigo']  # Elimina el código del estudiante 
    # Cerrar la sesión eliminando todos los datos de sesión
    request.session.flush()  # Esto elimina todos los datos de la sesión

    return redirect('login_page')  # Redirige a la página de inicio de sesión 

def dash_consejero(request):
    return render(request, 'consejeros/base.html')

def principal(request):
    return render(request, 'consejeros/home.html')



def perfil_consejero(request):
    codigo_docente = request.session.get('codigo_docente')
    if not codigo_docente:
        messages.error(request, 'No se encontró el código del consejero en la sesión.')
        return redirect('login')
    try:
        docente = docente.objects.get(codigo_docente=codigo_docente)
    except docente.DoesNotExist:
        messages.error(request, 'El consejero no esta registrado.')
        return redirect('login')
    context = {
        'docente': docente,
    }
    return render(request, 'consejeros/perfil.html', context)


def lista_matriculas_view(request):

    # Obtener el estado seleccionado desde el formulario
    estado = request.GET.get('estado', 'P')  # Por defecto es una cadena vacía
    
    # Filtrar matrículas por estado si se seleccionó alguno, si no, traer todas
    if estado:
        matriculas = Matricula.objects.filter(estado=estado).select_related('documentosmatricula').prefetch_related('semestre1', 'semestre2')
    else:
        # Obtener todas las matrículas con sus cursos y documentos
        matriculas = (
        Matricula.objects
        .select_related('documentosmatricula')  # OneToOneField
        .prefetch_related('semestre1', 'semestre2') # ManyToManyField
        .all()
        )
    return render(request, 'consejeros/revisar_matriculas.html', {'matriculas': matriculas, 'estado_seleccionado': estado})
def actualizar_matricula(request, matricula_id):
    if request.method == 'POST':
        matricula = get_object_or_404(Matricula, id=matricula_id)
        accion = request.POST.get('accion')

        if accion == 'aceptar':
            matricula.estado = 'Aceptado'
            messages.success(request, 'Matrícula aceptada.')
        elif accion == 'rechazar':
            matricula.estado = 'Rechazado'
            messages.warning(request, 'Matrícula rechazada.')          
            for curso in matricula.semestre1.all():
                curso.vacantes += 1
                curso.save()
            for curso in matricula.semestre2.all():
                curso.vacantes += 1
                curso.save()

        matricula.save()
        return redirect('listar')