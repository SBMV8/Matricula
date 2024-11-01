from django.db import models
from django.core.exceptions import ValidationError

class Usuario(models.Model):
    correo = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=128)
    rol = models.CharField(max_length=100, choices=[('estudiante', 'Estudiante'), ('administrativo', 'Administrativo'),('director', 'Director'),('docente', 'Docente')])

    def clean(self):
        if not self.correo.endswith('@unfv.edu.pe'):
            raise ValidationError("El correo debe pertenecer al dominio @unfv.edu.pe.")
    
    def __str__(self):
        return self.correo

class Estudiante(models.Model):
    codigo_estudiante = models.CharField(max_length=10, unique=True, primary_key=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    escuela = models.CharField(max_length=100)
    plan_estudios = models.CharField(max_length=4)
    nivel = models.IntegerField()
    ciclo = models.IntegerField()

    # Relación uno a uno con Usuario
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='estudiante')
    def __str__(self):
        return f"{self.nombres} {self.apellidos} ({self.codigo_estudiante})"

class Administrativo(models.Model):
    # Puedes agregar campos específicos para los administrativos si es necesario
    codigo_administrativo = models.CharField(max_length=10, unique=True, primary_key=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    
    # Relación uno a uno con Usuario
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='administrativo')

    def __str__(self):
        return f"{self.nombres} {self.apellidos} ({self.codigo_administrativo})"

class Director(models.Model):
    # Puedes agregar campos específicos para los administrativos si es necesario
    codigo_director = models.CharField(max_length=10, unique=True, primary_key=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    # Relación uno a uno con Usuario
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='director')

    def __str__(self):
        return f"{self.nombres} {self.apellidos} ({self.codigo_director})"
    
class Docente(models.Model):
    # Puedes agregar campos específicos para los administrativos si es necesario
    codigo_docente = models.CharField(max_length=10, unique=True, primary_key=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    escuela = models.CharField(max_length=100)
    
    # Relación uno a uno con Usuario
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='docente')

    def __str__(self):
        return f"{self.nombres} {self.apellidos} ({self.codigo_docente})"
