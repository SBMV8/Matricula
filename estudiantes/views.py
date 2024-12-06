from django.shortcuts import render,redirect
import os
from django.conf import settings
from django.core.paginator import Paginator
from .models import Curso, CursoAprobado,Matricula,DocumentosMatricula
from usuarios.models import Estudiante
from .forms import *
from django.contrib import messages

# Create your views here.

def estudiante_index(request):
    return render(request, 'estudiantes/index.html')

def logout_view(request):
    # Eliminar el código de estudiante de la sesión
    if 'codigo_estudiante' in request.session:
        del request.session['codigo_estudiante']  # Elimina el código del estudiante

    # Puedes eliminar otras variables de sesión si es necesario
    # del request.session['otra_variable']

    # Cerrar la sesión eliminando todos los datos de sesión
    request.session.flush()  # Esto elimina todos los datos de la sesión

    return redirect('login_page')  # Redirige a la página de inicio de sesión

def home(request):
    return render(request, 'estudiantes/home.html')

def consejeros(request):
    return render(request, 'estudiantes/consejeros.html')

def perfil(request):
    codigo_estudiante = request.session.get('codigo_estudiante')
    if not codigo_estudiante:
        messages.error(request, 'No se encontró el código del estudiante en la sesión.')
        return redirect('login')
    try:
        estudiante = Estudiante.objects.get(codigo_estudiante=codigo_estudiante)
    except Estudiante.DoesNotExist:
        messages.error(request, 'El estudiante no existe.')
        return redirect('login')
    context = {
        'estudiante': estudiante,
    }
    return render(request, 'estudiantes/perfil.html', context)


# Vista para mostrar los cursos en cursos.html
def cursos_view(request):
    cursos = Curso.objects.all()  
    paginator = Paginator(cursos, 15)  
    page_number = request.GET.get('page')  
    cursos = paginator.get_page(page_number) 
    return render(request, 'estudiantes/cursos.html', {'cursos': cursos})

# Vista para mostrar los registros de notas en registro_de_notas.html
def registro_de_notas_view(request):
    # Recuperamos el código de estudiante desde la sesión
    codigo_estudiante = request.session.get('codigo_estudiante')
    
    if not codigo_estudiante:
        # Manejar el caso donde no exista el código en la sesión
        return render(request, 'estudiantes/registro_de_notas.html', {'error': 'No se encontró el código de estudiante en la sesión.'})
    
    # Recuperamos el objeto Estudiante usando el código de estudiante
    try:
        estudiante = Estudiante.objects.get(codigo_estudiante=codigo_estudiante)
    except Estudiante.DoesNotExist:
        # Manejar el caso donde no exista el estudiante con ese código
        return render(request, 'estudiantes/registro_de_notas.html', {'error': 'El estudiante no existe.'})
    
    # Filtramos los cursos aprobados solo para ese estudiante
    cursos_aprobados = CursoAprobado.objects.filter(estudiante=estudiante)
    
    return render(request, 'estudiantes/registro_de_notas.html', {'cursos_aprobados': cursos_aprobados})

def pago_view(request):
    # Datos fijos
    monto = 2.00
    destinatario = "Güido Genaro Maidana Aquino"
    
    # Ruta de la imagen del QR almacenada en el sistema de archivos
    qr_image_path = os.path.join(settings.MEDIA_ROOT, 'qr_codes', 'pago_yape.jpg')

    # Verifica si la imagen existe
    if os.path.exists(qr_image_path):
        qr_image_url = os.path.join(settings.MEDIA_URL, 'qr_codes', 'pago_yape.jpg')
    else:
        qr_image_url = None  # En caso de que no se encuentre la imagen

    # Pasar datos a la plantilla
    context = {
        "monto": monto,
        "destinatario": destinatario,
        "qr_image_url": qr_image_url,  # Ruta de la imagen QR
    }

    return render(request, "estudiantes/pago.html", context)


def matricula_view(request):
    codigo_alumno = request.session.get('codigo_estudiante')

    if not codigo_alumno:
        messages.error(request, 'Error: No se encontró el código del estudiante.')
        return redirect('login')
    
    try:
        # Accede al estudiante utilizando el código directamente
        alumno = Estudiante.objects.get(codigo_estudiante=codigo_alumno)
    except Estudiante.DoesNotExist:
        messages.error(request, 'Error: Registro de alumno no encontrado.')
        return redirect('login')
    
    
    # Verificar si existe una matrícula pendiente o aprobada para el alumno
    matricula_existente = Matricula.objects.filter(codigo=alumno).exclude(estado='Rechazado').exists()

    if matricula_existente:
    # Si existe una matrícula pendiente o aprobada, mostrar mensaje de advertencia
        messages.warning(request, 'No puedes matricularte de nuevo porque tienes una matrícula pendiente o aprobada.')
        return redirect('perfil')  # Redirigir a la página que desees
    else:
    # Si no existe una matrícula pendiente o aprobada (es decir, fue rechazada), permitir la nueva matrícula
    # Lógica para permitir la nueva matrícula
        messages.success(request, 'procede con tu matricula')
    


    if request.method == 'POST':
        # Obtener los datos del formulario
        escuela = request.POST['escuela']
        plan = request.POST['plan']
        celular = request.POST['celular']
        num_recibo_primero = request.POST['num_recibo_primero']
        monto_recibo_primero = request.POST['monto_recibo_primero']
        num_recibo_segundo = request.POST['num_recibo_segundo']
        monto_recibo_segundo = request.POST['monto_recibo_segundo']

        # Obtener los archivos subidos desde el formulario
        recibo_pago_1 = request.FILES.get('recibo_pago_1')
        recibo_pago_2 = request.FILES.get('recibo_pago_2')
        boleta_notas = request.FILES.get('boleta_notas')

        # Obtener los cursos seleccionados
        cursos_semestre1 = []
        for i in range(1, 5):
            codigo = request.POST.get(f'curso1_{i}', None)
            if codigo:
                try:
                    curso = Curso.objects.get(codigo_curso=codigo)
                    if curso.vacantes > 0:
                        cursos_semestre1.append(curso)
                    else:
                        messages.error(request, f'El curso {curso.nombre} ya no tiene vacantes disponibles.')
                        return redirect('matricula')
                except Curso.DoesNotExist:
                    messages.error(request, f'Error: El curso con ID {codigo} no existe en el semestre 1.')
                    return redirect('matricula')
        
        cursos_semestre2 = []
        for i in range(1, 5):
            codigo = request.POST.get(f'curso2_{i}', None)
            if codigo:
                try:
                    curso = Curso.objects.get(codigo_curso=codigo)
                    if curso.vacantes > 0:
                       cursos_semestre2.append(curso)
                    else:
                        messages.error(request, f'El curso {curso.nombre} ya no tiene vacantes disponibles.')
                        return redirect('matricula')
                except Curso.DoesNotExist:
                    messages.error(request, f'Error: El curso con ID {codigo} no existe en el semestre 2.')
                    return redirect('matricula')

        # Validar y guardar la matrícula
        try:
            matricula = Matricula.objects.create(
                codigo=alumno,
                escuela=escuela,
                plan=plan,
                celular=celular,
                num_recibo_primero=num_recibo_primero,
                monto_recibo_primero=monto_recibo_primero,
                num_recibo_segundo=num_recibo_segundo,
                monto_recibo_segundo=monto_recibo_segundo,
            )
            matricula.semestre1.set(cursos_semestre1)
            matricula.semestre2.set(cursos_semestre2)
            matricula.save()

            # Reducir las vacantes de los cursos seleccionados
            for curso in cursos_semestre1 + cursos_semestre2:
                curso.vacantes -= 1
                curso.save()
            
            # Guardar documentos si existen
            if recibo_pago_1 or recibo_pago_2 or boleta_notas:
                documentos= DocumentosMatricula.objects.create(
                    matricula=matricula,
                    recibo_pago_1=recibo_pago_1,
                    recibo_pago_2=recibo_pago_2,
                    boleta_notas=boleta_notas,
                )
                print("Documentos guardados:", documentos)
            messages.success(request, 'Matrícula registrada exitosamente.')
            return redirect('matricula')
        except Exception as e:
            messages.error(request, f'Error: error al registrar la matricula:{str(e)}')

    # Obtener la información del alumno
    nivel_alumno = alumno.nivel
    primer_semestre_alumno = alumno.ciclo
    segundo_semestre_alumno = alumno.ciclo +1
    # Filtrar los cursos basados en el nivel y ciclo del estudiante
    cursos_semestre1 = Curso.objects.filter(nivel=nivel_alumno, ciclo=primer_semestre_alumno)
    cursos_semestre2 = Curso.objects.filter(nivel=nivel_alumno, ciclo=segundo_semestre_alumno)

    context = {
        'cursos_semestre1': cursos_semestre1,
        'cursos_semestre2': cursos_semestre2,
        'nombre': alumno.nombres,
        'apellido': alumno.apellidos,
        'codigo': alumno.codigo_estudiante,
    }
    return render(request, 'estudiantes/Matricula.html', context)

# def save(self, *args, **kwargs):
#     # Detectar si el estado ha cambiado a RECHAZADO
#     if self.pk:  # Verificar si es una actualización
#         matricula_anterior = Matricula.objects.get(pk=self.pk)
#         if matricula_anterior.estado != self.RECHAZADO and self.estado == self.RECHAZADO:
#             self.rechazar_matricula()  # Llama a la función de rechazo

#     super(Matricula, self).save(*args, **kwargs)




# def rechazar_matricula(request, matricula_id):
#     try:
#         matricula = Matricula.objects.get(id=matricula_id)
        
#         # Cambiar el estado solo si es 'Pendiente'
#         if matricula.estado == 'Pendiente':
#             # Aumentar las vacantes de los cursos en la matrícula
#             for curso in matricula.semestre1.all():
#                 curso.vacantes += 1
#                 curso.save()

#             for curso in matricula.semestre2.all():
#                 curso.vacantes += 1
#                 curso.save()

#             # Cambiar el estado de la matrícula
#             matricula.estado = 'Rechazado'  # Cambia el estado aquí
#             matricula.save()

#             messages.success(request, 'Matrícula rechazada y vacantes actualizadas.')
#         else:
#             messages.warning(request, 'Solo se puede rechazar una matrícula pendiente.')

#     except Matricula.DoesNotExist:
#         messages.error(request, 'Matrícula no encontrada.')


def Documentos_view(request):
    codigo_alumno = request.session.get('codigo_estudiante')

    if not codigo_alumno:
        messages.error(request, 'Error: No se encontró el código del estudiante.')
        return redirect('login')
    
    try:
        # Accede al estudiante utilizando el código directamente
        alumno = Estudiante.objects.get(codigo_estudiante=codigo_alumno)
    except Estudiante.DoesNotExist:
        messages.error(request, 'Error: Registro de alumno no encontrado.')
        return redirect('login')
    
    # Intentar obtener la matrícula del alumno
    try:
        matricula = Matricula.objects.get(codigo=alumno)
    except Matricula.DoesNotExist:
        messages.error(request, 'Error: No se encontró la matrícula del estudiante.')
        return redirect('perfil')
    
    if request.method == 'POST':
        # Obtener los archivos subidos desde el formulario
        recibo_pago_1 = request.FILES.get('recibo_pago_1')
        recibo_pago_2 = request.FILES.get('recibo_pago_2')
        boleta_notas = request.FILES.get('boleta_notas')

        # Validar y guardar la matrícula
        try:

            # Guardar documentos si existen
            if recibo_pago_1 or recibo_pago_2 or boleta_notas:
                DocumentosMatricula.objects.create(
                    matricula=matricula,
                    recibo_pago_1=recibo_pago_1,
                    recibo_pago_2=recibo_pago_2,
                    boleta_notas=boleta_notas,
                )
            messages.success(request, 'documentos registrados exitosamente.')
            return redirect('perfil.html')
        except Exception as e:
            messages.error(request, f'Error: error al registrar:{str(e)}')

    
    return render(request, 'estudiantes/perfil.html')