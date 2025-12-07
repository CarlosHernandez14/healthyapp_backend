from django.db import models

# Create your models here.
class Paciente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)

    edad = models.PositiveIntegerField(null=True, blank=True)
    genero = models.CharField(max_length=20, null=True, blank=True)
    
    def __str__(self):
        return f'{self.nombre} {self.apellido}'