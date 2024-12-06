from django.db import models
from usuarios.models import Estudiante  # Importamos el modelo Estudiante desde la app Usuarios


class Curso(models.Model):
    codigo_curso = models.CharField(max_length=10, unique=True, primary_key=True)
    nombre = models.CharField(max_length=100)
    creditos = models.IntegerField()
    nivel = models.IntegerField()  # Año académico
    ciclo = models.IntegerField()  # Ciclo dentro del nivel
    pre_requisito = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='cursos_requeridos')
    vacantes = models.PositiveIntegerField(default=30)
    
    def __str__(self):
        return f"{self.nombre} ({self.codigo_curso})"

    class Meta:
        ordering = ['nivel', 'ciclo', 'codigo_curso']


class CursoAprobado(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name='cursos_aprobados')  # Relación con Estudiante desde Usuarios
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='estudiantes_aprobados')
    fecha_aprobacion = models.DateField()
    nota = models.DecimalField(max_digits=5, decimal_places=2)  # Nota del curso, de 1 a 20
    aprobado = models.BooleanField(default=False)  # Campo para indicar si aprobó o no

    def save(self, *args, **kwargs):
        # Establece el valor de 'aprobado' basado en la nota
        self.aprobado = self.nota >= 10.5  # Consideramos aprobado si la nota es 10.5 o mayor
        super().save(*args, **kwargs)  # Llama al método save de la clase padre

    def __str__(self):
        return f"{self.estudiante} aprobó {self.curso} - {'Aprobado' if self.aprobado else 'No Aprobado'}"

    class Meta:
        unique_together = ('estudiante', 'curso')  # Evitar duplicados
        
class TransaccionPago(models.Model):
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Aceptado', 'Aceptado'),
        ('Rechazado', 'Rechazado'),
    ]

    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name="transacciones")
    numero_transaccion = models.CharField(max_length=50)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='Pendiente')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transacción {self.numero_transaccion} - {self.estudiante.codigo_estudiante} ({self.estado})"

class Matricula(models.Model):
    # Relación con la tabla Registro para heredar el código del alumno
    codigo = models.ForeignKey(Estudiante, on_delete=models.CASCADE, to_field='codigo_estudiante')
    
    # Información adicional
    escuela = models.CharField(max_length=100)  
    plan = models.CharField(max_length=4)  
    celular = models.CharField(max_length=9)  
    num_recibo_primero = models.CharField(max_length=20)  # Número del primer recibo
    num_recibo_segundo = models.CharField(max_length=20)  # Número del segundo recibo
    monto_recibo_primero = models.DecimalField(max_digits=10, decimal_places=2)  # Monto del primer recibo
    monto_recibo_segundo = models.DecimalField(max_digits=10, decimal_places=2)  # Monto del segundo recibo

    # Relación ManyToMany para cursos
    semestre1 = models.ManyToManyField(Curso, related_name='matriculas_semestre1') 
    semestre2 = models.ManyToManyField(Curso, related_name='matriculas_semestre2')  # Cambiado a ManyToManyField

    # Fecha de la matrícula
    fecha_matricula = models.DateField(auto_now_add=True)

    # Campo para estado
    PENDIENTE = 'P'
    ACEPTADO = 'A'
    RECHAZADO = 'R'

    ESTADO_CHOICES = [
        (PENDIENTE, 'Pendiente'),
        (ACEPTADO, 'Aceptado'),
        (RECHAZADO, 'Rechazado'),
    ]
    
    estado = models.CharField(
        max_length=1,
        choices=ESTADO_CHOICES,
        default=PENDIENTE,
    )

    def __str__(self):
        return f"Matricula de {self.codigo.nombres} {self.codigo.apellidos}"

class DocumentosMatricula(models.Model):
    matricula = models.OneToOneField(Matricula, on_delete=models.CASCADE)  # Si se elimina la matrícula, también se eliminan los documentos
    recibo_pago_1 = models.FileField(upload_to='documentos/', default='default.pdf')
    recibo_pago_2 = models.FileField(upload_to='documentos/', default='default.pdf')
    boleta_notas = models.FileField(upload_to='documentos/', default='default.pdf')

    def __str__(self):
        return f'Documentos de Matricula con ID: {self.matricula.id}'

