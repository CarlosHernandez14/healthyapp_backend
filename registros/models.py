from django.db import models
from citas.models import Cita
# Create your models here.

class RegistroDiario(models.Model):
    cita = models.ForeignKey(Cita, on_delete=models.CASCADE, related_name='resgistros')
    fecha = models.DateField()
    cumplio = models.BooleanField(default=False)
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.cita} - {self.fecha}" 
