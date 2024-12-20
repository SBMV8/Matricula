from django.contrib import admin
from .models import Usuario, Estudiante, Administrativo, Docente, Director

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('correo', 'password','rol')
    search_fields = ('correo',)

@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ('codigo_estudiante', 'nombres', 'apellidos', 'get_correo', 'escuela', 'nivel', 'ciclo')
    search_fields = ('codigo_estudiante', 'nombres', 'apellidos')

    def get_correo(self, obj):
        return obj.usuario.correo  # Accede al campo correo del modelo Usuario
    get_correo.short_description = 'Correo'  # Nombre que aparecerá en la columna

@admin.register(Administrativo)
class AdministrativoAdmin(admin.ModelAdmin):
    list_display = ('codigo_administrativo', 'nombres', 'apellidos', 'get_correo', 'telefono')
    search_fields = ('codigo_administrativo', 'nombres', 'apellidos')

    def get_correo(self, obj):
        return obj.usuario.correo  # Accede al campo correo del modelo Usuario
    get_correo.short_description = 'Correo'  # Nombre que aparecerá en la columna

@admin.register(Docente)
class DocenteAdmin(admin.ModelAdmin):
    list_display = ('codigo_docente', 'nombres', 'apellidos', 'get_correo', 'escuela','telefono')
    search_fields = ('codigo_docente', 'nombres', 'apellidos')

    def get_correo(self, obj):
        return obj.usuario.correo  # Accede al campo correo del modelo Usuario
    get_correo.short_description = 'Correo'  # Nombre que aparecerá en la columna
@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ('codigo_director', 'nombres', 'apellidos', 'get_correo','telefono')
    search_fields = ('codigo_director', 'nombres', 'apellidos')

    def get_correo(self, obj):
        return obj.usuario.correo  # Accede al campo correo del modelo Usuario
    get_correo.short_description = 'Correo'  # Nombre que aparecerá en la columna



