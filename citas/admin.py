from django.contrib import admin
from .models import Cita

@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'fecha', 'hora', 'tipo', 'estado')
    list_filter = ('estado', 'tipo', 'fecha')
    search_fields = ('paciente__nombre', 'paciente__apellido', 'motivo')
