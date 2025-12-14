from django.shortcuts import render

from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from .models import Cita
from .serializers import CitaSerializer

class CitaPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class CitaViewSet(viewsets.ModelViewSet):
    queryset = Cita.objects.select_related('paciente').all()
    serializer_class = CitaSerializer
    pagination_class = CitaPagination
    permission_classes = [IsAuthenticated]

    # Filtros por paciente, tipo, estado y rango de fechas (YYYY-MM-DD)
    # Soporta nombres de parámetros nuevos (fecha_inicio, fecha_fin) y legacy (desde, hasta).
    def get_queryset(self):
        qs = super().get_queryset()
        params = self.request.query_params

        # Paciente
        paciente_id = params.get('paciente')
        if paciente_id:
            qs = qs.filter(paciente_id=paciente_id)

        # Tipo de cita (valores del modelo: 'primera', 'seguimiento')
        tipo = params.get('tipo')
        if tipo:
            qs = qs.filter(tipo=tipo)

        # Estado de la cita
        estado = params.get('estado')
        if estado:
            qs = qs.filter(estado=estado)

        # Rango de fechas
        fecha_inicio = params.get('fecha_inicio') or params.get('desde')
        if fecha_inicio:
            qs = qs.filter(fecha__gte=fecha_inicio)

        fecha_fin = params.get('fecha_fin') or params.get('hasta')
        if fecha_fin:
            qs = qs.filter(fecha__lte=fecha_fin)

        return qs
