from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .models import Usuario, Estudiante, Administrativo,Director,Docente


# Create your views here.

def login(request):
    if request.method == 'POST':
        correo = request.POST.get('logemail')
        password = request.POST.get('logpass')
        
        # Verificar si el usuario existe en la base de datos
        try:
            usuario = Usuario.objects.get(correo=correo, password=password)  # Aquí deberías usar un método de hash para la contraseña
            # Si llega aquí, el usuario existe y la contraseña es correcta
           
            # Verificar el rol y redirigir
            if usuario.rol == 'estudiante':
                # Guarda el código en la sesión
                alumno = Estudiante.objects.get(usuario=usuario) 
                request.session['codigo_estudiante'] = alumno.codigo_estudiante  
                return redirect('estudiante_index')  # Cambia esto por la URL de la vista de estudiantes
            elif usuario.rol == 'administrativo':
                administrativo = Administrativo.objects.get(usuario=usuario)
                request.session['codigo_administrativo'] = administrativo.codigo_administrativo
                return redirect('administrativo_index')  # Cambia esto por la URL de la vista de administrativos
            elif usuario.rol == 'director':
                director = Director.objects.get(usuario=usuario)
                request.session['codigo_director'] = director.codigo_director
                return redirect('director_index')
            elif usuario.rol == 'docente':
                docente =Docente.objects.get(usuario=usuario)
                request.session['codigo_docente'] = docente.codigo_docente
                return redirect('consejero_index')
        except Usuario.DoesNotExist:
            messages.error(request, 'Credenciales incorrectas')
    
    return render(request, 'usuarios/login.html')


@csrf_exempt
def change_password(request):
    if request.method == 'POST':
        correo = request.POST.get('logemail')
        nueva_contraseña = request.POST.get('newpass')
        try:
            usuario = Usuario.objects.get(correo=correo)
        except Usuario.DoesNotExist:
            messages.error(request, 'El correo ingresado no está registrado en nuestro sistema.')
            return redirect('change_password') 
        if len(nueva_contraseña) < 8:
            messages.error(request, 'La contraseña debe tener al menos 8 caracteres.')
            return redirect('change_password')  
        usuario.password = nueva_contraseña
        usuario.save()

        messages.success(request, '¡Contraseña cambiada exitosamente! Por favor, inicia sesión con tu nueva contraseña.')
        return redirect('login')  

    return render(request, 'usuarios/login.html')

