from django.contrib import admin
from .models import Cita

@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'fecha', 'hora', 'tipo', 'estado', 'enfoque_nutricional')
    list_filter = ('estado', 'tipo', 'fecha', 'enfoque_nutricional')
    search_fields = ('paciente__nombre', 'paciente__apellido', 'motivo', 'enfoque_nutricional', 'objetivo_nutricional', 'plan_alimentacion', 'recomendaciones')
