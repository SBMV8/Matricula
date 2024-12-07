from django.shortcuts import render, redirect,get_object_or_404
from django.core.paginator import Paginator
from estudiantes.models import Curso
from usuarios.models import Estudiante, Administrativo, Usuario,Docente,Director
from estudiantes.models import Matricula, DocumentosMatricula, TransaccionPago
from django.contrib import messages
# Create your views here.

def consejero_index(request):
    return render(request, 'consejeros/index.html')

def logout_view(request):
    # Eliminar el código de estudiante de la sesión
    if 'codigo_consejero' in request.session:
        del request.session['codigo_consejero']  # Elimina el código del consejero
    # Cerrar la sesión eliminando todos los datos de sesión
    request.session.flush()  # Esto elimina todos los datos de la sesión

    return redirect('login_page')  # Redirige a la página de inicio de sesión 

def home(request):
    return render(request, 'consejeros/home.html')

def perfil_consejero(request):
    codigo_docente = request.session.get('codigo_docente')
    if not codigo_docente:
        messages.error(request, 'No se encontró el código del consejero en la sesión.')
        return redirect('login')
    try:
        docente = Docente.objects.get(codigo_docente=codigo_docente)
    except Docente.DoesNotExist:
        messages.error(request, 'El consejero no existe.')
        return redirect('login')
    context = {
        'docente': docente,
    }
    return render(request, 'consejeros/perfil.html', context)

def verificar_pagos_view(request):
    # Obtener el estado seleccionado desde el formulario GET
    estado = request.GET.get('estado', 'Pendiente')  # Por defecto, filtra por "Pendiente"

    # Filtrar las transacciones por estado si se seleccionó alguno
    if estado:
        transacciones = TransaccionPago.objects.filter(estado=estado).select_related('estudiante')
    else:
        # Obtener todas las transacciones si no se especifica el estado
        transacciones = TransaccionPago.objects.select_related('estudiante').all()

    # Manejar acciones POST (Aceptar o Rechazar)
    if request.method == "POST":
        transaccion_id = request.POST.get("transaccion_id")
        accion = request.POST.get("accion")

        try:
            transaccion = TransaccionPago.objects.get(id=transaccion_id)
            if accion == "aceptar":
                transaccion.estado = "Aceptado"
                messages.success(request, f"Transacción {transaccion.numero_transaccion} aceptada.")
            elif accion == "rechazar":
                transaccion.estado = "Rechazado"
                messages.warning(request, f"Transacción {transaccion.numero_transaccion} rechazada.")
            transaccion.save()
        except TransaccionPago.DoesNotExist:
            messages.error(request, "La transacción no existe.")
        except Exception as e:
            messages.error(request, f"Error al procesar la transacción: {e}")

        return redirect('verificar_pagos')

    # Renderizar el template con las transacciones y el estado seleccionado
    context = {
        "transacciones": transacciones,
        "estado_seleccionado": estado,
    }
    return render(request, 'consejeros/verificar_pagos.html', context)

def actualizar_pago(request, transaccion_id):
    if request.method == "POST":
        accion = request.POST.get("accion")
        transaccion = get_object_or_404(TransaccionPago, id=transaccion_id)

        if accion == "aceptar":
            transaccion.estado = "Aceptado"
            messages.success(request, f"Transacción {transaccion.numero_transaccion} aceptada.")
        elif accion == "rechazar":
            transaccion.estado = "Rechazado"
            messages.warning(request, f"Transacción {transaccion.numero_transaccion} rechazada.")
        else:
            messages.error(request, "Acción no válida.")

        transaccion.save()
        return redirect('verificar_pagos')
    
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