from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistroUsuarioForm
from usuarios.models import Estudiante, Usuario, Docente,Director
# Create your views here.

def director_index(request):
    return render(request, 'director/index.html')

def logout_vista(request):
    if 'codigo_director' in request.session:
        del request.session['codigo_director']  
    request.session.flush() 
    return redirect('login')

def base_director(request):
    return render(request, 'director/base.html')

def principal(request):
    return render(request, 'director/home.html')


def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            # Campos adicionales
            codigo = form.cleaned_data.get('codigo')
            nombres = form.cleaned_data.get('nombres')
            apellidos = form.cleaned_data.get('apellidos')
            telefono = form.cleaned_data.get('telefono')

            # Dependiendo del rol, creamos un Estudiante o Administrativo
            if usuario.rol == 'estudiante':
                escuela = form.cleaned_data.get('escuela')
                plan_estudios = form.cleaned_data.get('plan_estudios')
                nivel = form.cleaned_data.get('nivel')
                ciclo = form.cleaned_data.get('ciclo')

                # Crear el registro de estudiante
                Estudiante.objects.create(
                    usuario=usuario,
                    codigo_estudiante=codigo,
                    nombres=nombres,
                    apellidos=apellidos,
                    telefono=telefono,
                    escuela=escuela,
                    plan_estudios=plan_estudios,
                    nivel=nivel,
                    ciclo=ciclo
                )
            elif usuario.rol == 'docente':
                escuela = form.cleaned_data.get('escuela')
                # Crear el registro de docente
                Docente.objects.create(
                    usuario=usuario,
                    codigo_docente=codigo,
                    nombres=nombres,
                    apellidos=apellidos,
                    telefono=telefono,
                    escuela=escuela,
                )
            
            return redirect('registro')  
    else:
        form = RegistroUsuarioForm()
        usuarios = Usuario.objects.filter(rol__in=['docente', 'estudiante'])
    
    return render(request, 'director/registro_usuario.html', {
        'form': form,
        'usuarios': usuarios,  
    })

def perfil_director(request):
    codigo_director = request.session.get('codigo_director')
    if not codigo_director:
        messages.error(request, 'No se encontró el código del administrativo en la sesión.')
        return redirect('login')
    try:
        director = Director.objects.get(codigo_director=codigo_director)
    except Director.DoesNotExist:
        messages.error(request, 'El director no existe.')
        return redirect('login')
    context = {
        'director': director,
    }
    return render(request, 'director/perfil.html', context)


# Create your views here.
