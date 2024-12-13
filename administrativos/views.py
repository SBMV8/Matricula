from django.shortcuts import render, redirect,get_object_or_404
from django.core.paginator import Paginator
from estudiantes.models import Curso, Matricula, CursoAprobado
from .forms import RegistroUsuarioForm
from usuarios.models import Estudiante, Administrativo, Usuario, Docente, Director
from django.contrib import messages
from django.http import JsonResponse
import pandas as pd
# Create your views here.

def administrativo_index(request):
    return render(request, 'administrativos/index.html')

def logout_vista(request):
    if 'codigo_administrativo' in request.session:
        del request.session['codigo_administrativo']  
    request.session.flush() 
    return redirect('login')

def dash_admi(request):
    return render(request, 'administrativos/dash.html')

def principal(request):
    return render(request, 'administrativos/home.html')

def registro_usuario(request):
    if request.method == 'POST':
        if 'excel_file' in request.FILES:  # Verificar si se subió un archivo
            excel_file = request.FILES['excel_file']
            if not excel_file:
                messages.error(request, "Por favor, selecciona un archivo.")
                return redirect("registro_usuario")
            try:
                # Leer el archivo Excel con pandas
                data = pd.read_excel(excel_file)
                
                # Procesar cada fila del Excel
                for _, row in data.iterrows():
                    # Crear un usuario
                    usuario = Usuario.objects.create(
                        correo=row.get('correo'),
                        password=row.get('password'),  
                        rol=row.get('rol'),
                    )

                    # Campos comunes
                    codigo = row.get('codigo')
                    nombres = row.get('nombres')
                    apellidos = row.get('apellidos')
                    telefono = row.get('telefono')

                    # Verifica el rol y crea el modelo específico
                    if usuario.rol == 'estudiante':
                        Estudiante.objects.create(
                            usuario=usuario,
                            codigo_estudiante=codigo,
                            nombres=nombres,
                            apellidos=apellidos,
                            telefono=telefono,
                            escuela=row.get('escuela'),
                            plan_estudios=row.get('plan_estudios'),
                            nivel=row.get('nivel'),
                            ciclo=row.get('ciclo'),
                        )
                    elif usuario.rol == 'administrativo':
                        Administrativo.objects.create(
                            usuario=usuario,
                            codigo_administrativo=codigo,
                            nombres=nombres,
                            apellidos=apellidos,
                            telefono=telefono,
                        )
                    elif usuario.rol == 'director':
                        Director.objects.create(
                            usuario=usuario,
                            codigo_director=codigo,
                            nombres=nombres,
                            apellidos=apellidos,
                            telefono=telefono,
                        )
                    elif usuario.rol == 'docente':
                        Docente.objects.create(
                            usuario=usuario,
                            codigo_docente=codigo,
                            nombres=nombres,
                            apellidos=apellidos,
                            telefono=telefono,
                            escuela=row.get('escuela'),
                        )
                
                messages.success(request, "Usuarios registrados exitosamente.")
                return redirect('registro_usuario')
            except Exception as e:
                # Manejar errores en la lectura del archivo
                messages.error(request, f"Error al procesar el archivo: {str(e)}")
                return redirect("registro_usuario")
        else:
            # Procesar el formulario manualmente
            form = RegistroUsuarioForm(request.POST)
            if form.is_valid():
                try:
                    usuario = form.save()
                    # Campos comunes
                    codigo = form.cleaned_data.get('codigo')
                    nombres = form.cleaned_data.get('nombres')
                    apellidos = form.cleaned_data.get('apellidos')
                    telefono = form.cleaned_data.get('telefono')

                    # Creación según el rol
                    if usuario.rol == 'estudiante':
                        Estudiante.objects.create(
                            usuario=usuario,
                            codigo_estudiante=codigo,
                            nombres=nombres,
                            apellidos=apellidos,
                            telefono=telefono,
                            escuela=form.cleaned_data.get('escuela'),
                            plan_estudios=form.cleaned_data.get('plan_estudios'),
                            nivel=form.cleaned_data.get('nivel'),
                            ciclo=form.cleaned_data.get('ciclo')
                        )
                    elif usuario.rol == 'administrativo':
                        Administrativo.objects.create(
                            usuario=usuario,
                            codigo_administrativo=codigo,
                            nombres=nombres,
                            apellidos=apellidos,
                            telefono=telefono
                        )
                    elif usuario.rol == 'director':
                        Director.objects.create(
                            usuario=usuario,
                            codigo_director=codigo,
                            nombres=nombres,
                            apellidos=apellidos,
                            telefono=telefono
                        )
                    elif usuario.rol == 'docente':
                        Docente.objects.create(
                            usuario=usuario,
                            codigo_docente=codigo,
                            nombres=nombres,
                            apellidos=apellidos,
                            telefono=telefono,
                            escuela=form.cleaned_data.get('escuela')
                        )

                    messages.success(request, "Usuario registrado exitosamente.")
                    return redirect('registro_usuario')
                except Exception as e:
                    messages.error(request, f"Error al registrar el usuario: {str(e)}")
            else:
                messages.error(request, "Por favor corrige los errores en el formulario.")
    
    form = RegistroUsuarioForm()
    usuarios = Usuario.objects.all()
    return render(request, 'administrativos/registro_usuario.html', {'form': form, 'usuarios': usuarios})

def perfil_admi(request):
    codigo_administrativo = request.session.get('codigo_administrativo')
    if not codigo_administrativo:
        messages.error(request, 'No se encontró el código del administrativo en la sesión.')
        return redirect('login')
    try:
        administrativo = Administrativo.objects.get(codigo_administrativo=codigo_administrativo)
    except Administrativo.DoesNotExist:
        messages.error(request, 'El administrativo no existe.')
        return redirect('login')
    context = {
        'administrativo': administrativo,
    }
    return render(request, 'administrativos/perfil.html', context)

def registrar_cursos(request):
    if request.method == 'POST':
        codigo_curso = request.POST.get('codigo_curso')
        nombre = request.POST.get('nombre')
        creditos = request.POST.get('creditos')
        nivel = request.POST.get('nivel')
        ciclo = request.POST.get('ciclo')
        prerrequisito_codigo = request.POST.get('prerrequisito')
        prerrequisito = None
        vacantes =request.POST.get('vacantes')
        if prerrequisito_codigo:
            try:
                prerrequisito = Curso.objects.get(codigo_curso=prerrequisito_codigo)
            except Curso.DoesNotExist:
                prerrequisito = None  
        Curso.objects.create(
            codigo_curso=codigo_curso,
            nombre=nombre,
            creditos=creditos,
            nivel=nivel,
            ciclo=ciclo,
            pre_requisito=prerrequisito,
            vacantes=vacantes
        )

        return redirect('registrar_cursos') 

    cursos = Curso.objects.all()  
    paginator = Paginator(cursos, 12)  
    page_number = request.GET.get('page')  
    cursos = paginator.get_page(page_number)  
    return render(request, 'administrativos/registro_cursos.html', {'cursos': cursos})


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
    return render(request, 'administrativos/revisar_matriculas.html', {'matriculas': matriculas, 'estado_seleccionado': estado})
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
    
def editar_usuario(request, user_id):
    usuario = get_object_or_404(Usuario, id=user_id)

    if request.method == 'POST':
        usuario.correo = request.POST.get('correo', usuario.correo)

        if usuario.rol == 'estudiante':
            estudiante = usuario.estudiante
            estudiante.nombres = request.POST.get('nombres', estudiante.nombres)
            estudiante.apellidos = request.POST.get('apellidos', estudiante.apellidos)
            estudiante.telefono = request.POST.get('telefono', estudiante.telefono)
            estudiante.escuela = request.POST.get('escuela', estudiante.escuela)
            estudiante.plan_estudios = request.POST.get('plan_estudios', estudiante.plan_estudios)
            estudiante.nivel = request.POST.get('nivel', estudiante.nivel)
            estudiante.ciclo = request.POST.get('ciclo', estudiante.ciclo)
            estudiante.save()
        elif usuario.rol == 'administrativo':
            administrativo = usuario.administrativo
            administrativo.nombres = request.POST.get('nombres', administrativo.nombres)
            administrativo.apellidos = request.POST.get('apellidos', administrativo.apellidos)
            administrativo.telefono = request.POST.get('telefono', administrativo.telefono)
            administrativo.save()
        elif usuario.rol == 'director':
            director = usuario.director
            director.nombres = request.POST.get('nombres', director.nombres)
            director.apellidos = request.POST.get('apellidos', director.apellidos)
            director.telefono = request.POST.get('telefono', director.telefono)
            director.save()
        elif usuario.rol == 'docente':
            docente = usuario.docente
            docente.nombres = request.POST.get('nombres', docente.nombres)
            docente.apellidos = request.POST.get('apellidos', docente.apellidos)
            docente.telefono = request.POST.get('telefono', docente.telefono)
            docente.escuela = request.POST.get('escuela', docente.escuela)
            docente.save()

        usuario.save()
        return redirect('registro_usuario')

    # Datos para el formulario de edición
    data = {
        'usuario': usuario,
        'nombres': getattr(usuario, usuario.rol).nombres,
        'correo': usuario.correo,
        'rol': usuario.rol
    }

    if usuario.rol == 'estudiante':
        estudiante = usuario.estudiante
        data.update({
            'codigo': estudiante.codigo_estudiante,
            'apellidos': estudiante.apellidos,
            'telefono': estudiante.telefono,
            'escuela': estudiante.escuela,
            'plan_estudios': estudiante.plan_estudios,
            'nivel': estudiante.nivel,
            'ciclo': estudiante.ciclo,
        })
    elif usuario.rol == 'administrativo':
        administrativo = usuario.administrativo
        data.update({
            'codigo': administrativo.codigo_administrativo,
            'apellidos': administrativo.apellidos,
            'telefono': administrativo.telefono,
        })
    elif usuario.rol == 'director':
        director = usuario.director
        data.update({
            'codigo': director.codigo_director,
            'apellidos': director.apellidos,
            'telefono': director.telefono,
        })
    elif usuario.rol == 'docente':
        docente = usuario.docente
        data.update({
            'codigo': docente.codigo_docente,
            'apellidos': docente.apellidos,
            'telefono': docente.telefono,
            'escuela': docente.escuela,
        })

    return render(request, 'administrativos/editar_usuario.html', {'data': data})

def eliminar_usuario(request, user_id):
    usuario = get_object_or_404(Usuario, id=user_id)
    if request.method == 'DELETE':
        usuario.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'fail'}, status=400)

def obtener_usuario(user_id):
    usuario = get_object_or_404(Usuario, id=user_id)
    data = {
        'id': usuario.id,
        'correo': usuario.correo,
        'rol': usuario.rol,
    }

    if usuario.rol == 'estudiante':
        estudiante = usuario.estudiante
        data.update({
            'codigo': estudiante.codigo_estudiante,
            'nombres': estudiante.nombres,
            'apellidos': estudiante.apellidos,
            'telefono': estudiante.telefono,
            'escuela': estudiante.escuela,
            'plan_estudios': estudiante.plan_estudios,
            'nivel': estudiante.nivel,
            'ciclo': estudiante.ciclo,
        })
    elif usuario.rol == 'administrativo':
        administrativo = usuario.administrativo
        data.update({
            'codigo': administrativo.codigo_administrativo,
            'nombres': administrativo.nombres,
            'apellidos': administrativo.apellidos,
            'telefono': administrativo.telefono,
        })

    elif usuario.rol == 'director':
        director = usuario.director
        data.update({
            'codigo': director.codigo_director,
            'apellidos': director.apellidos,
            'telefono': director.telefono,
        })
    elif usuario.rol == 'docente':
        docente = usuario.docente
        data.update({
            'codigo': docente.codigo_docente,
            'apellidos': docente.apellidos,
            'telefono': docente.telefono,
            'escuela': docente.escuela,
        })

    return JsonResponse(data)

def registro_notas(request):
    if request.method == 'POST':
        estudiante_id = request.POST.get('estudiante')
        curso_id = request.POST.get('curso')
        fecha_aprobacion = request.POST.get('fecha_aprobacion')
        nota = request.POST.get('nota')

        # Convertir nota a float
        try:
            nota = float(nota)  # Convertir la nota a float
        except ValueError:
            return render(request, 'administrativos/registro_notas.html', {
                'estudiantes': Estudiante.objects.all(),
                'cursos': Curso.objects.all(),
                'error': 'La nota debe ser un número válido.'
            })

        # Obtener el estudiante y el curso
        estudiante = Estudiante.objects.get(codigo_estudiante=estudiante_id)
        curso = Curso.objects.get(codigo_curso=curso_id)

        # Crear una nueva instancia de CursoAprobado
        curso_aprobado = CursoAprobado(
            estudiante=estudiante,
            curso=curso,
            fecha_aprobacion=fecha_aprobacion,
            nota=nota
        )
        curso_aprobado.save()

        return redirect('registro_notas')  

    estudiantes = Estudiante.objects.all()  
    cursos = Curso.objects.all()  
    return render(request, 'administrativos/registro_notas.html', {
        'estudiantes': estudiantes, 
        'cursos': cursos
    })
