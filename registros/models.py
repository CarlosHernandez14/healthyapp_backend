from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from citas.models import Cita
# Create your models here.

class RegistroDiario(models.Model):
    cita = models.ForeignKey(Cita, on_delete=models.CASCADE, related_name='registros')
    fecha = models.DateField()
    cumplio = models.BooleanField(default=False)
    observaciones = models.TextField(blank=True, null=True)
    # Nutrición - métricas diarias opcionales (mantener simple para proyecto final)
    calorias = models.PositiveIntegerField(null=True, blank=True)
    agua_ml = models.PositiveIntegerField(null=True, blank=True)
    actividad_min = models.PositiveIntegerField(null=True, blank=True)
    peso_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    adherencia = models.PositiveSmallIntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.cita} - {self.fecha}"
