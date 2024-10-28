"""
URL configuration for FIIS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from usuarios import views as usuarios_views
from estudiantes import views as estudiantes_views
from administrativos import views as administrativos_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Rutas para el inicio de sesión
    path('', usuarios_views.login, name='login'),  # Ruta principal para el login
    path('login/', usuarios_views.login, name='login_page'),  # Ruta específica para el login
    path('logout/', estudiantes_views.logout_view, name='logout_view'),  # Ruta para el cierre de sesión
    path('change_password/', usuarios_views.change_password, name='change_password'),  # Ruta para cambiar la contraseña
    
    # Rutas para el rol de estudiante
    path('estudiante/index/', estudiantes_views.estudiante_index, name='estudiante_index'), 
    path('estudiante/home/', estudiantes_views.home, name='home'),  
    path('estudiante/perfil/', estudiantes_views.perfil, name='perfil'), 
    path('estudiante/consejeros/', estudiantes_views.consejeros, name='consejeros'), 
    path('estudiante/cursos/', estudiantes_views.cursos_view, name='cursos'),
    path('estudiante/registro-de-notas/', estudiantes_views.registro_de_notas_view, name='registro_de_notas'),
    path('estudiante/matricula/', estudiantes_views.matricula_view, name='matricula'),
    path('estudiante/prueba/', estudiantes_views.Documentos_view, name='prueba'),
    
    # Rutas para el rol de administrativo
    path('administrativo/index/', administrativos_views.administrativo_index, name='administrativo_index'), 
    path('administrativo/logout_vista/', administrativos_views.logout_vista, name='logout_vista'),  
    path('administrativo/dash_admi/', administrativos_views.dash_admi, name='dash_admi'),  
    path('administrativo/principal/', administrativos_views.principal, name='principal'),  
    path('administrativo/perfil_admi/', administrativos_views.perfil_admi, name='perfil_admi'),  
    path('administrativo/registrar_cursos/',administrativos_views.registrar_cursos, name='registrar_cursos'),
    path('administrativo/registro_usuario/', administrativos_views.registro_usuario, name='registro_usuario'),
    path('administrativo/revisar_matriculas/', administrativos_views.lista_matriculas_view, name='listar'),
    path('administrativo/actualizar_matricula/<int:matricula_id>/', administrativos_views.actualizar_matricula, name='actualizar_matricula'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


