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
    queryset = Cita.objects.all()
    serializer_class = CitaSerializer
    pagination_class = CitaPagination
    permission_classes = [IsAuthenticated]

    # Filtros por paciente, estado y rango de fechas (YYYY-MM-DD)
    def get_queryset(self):
        qs = super().get_queryset()
        params = self.request.query_params

        paciente_id = params.get('paciente')
        if paciente_id:
            qs = qs.filter(paciente_id=paciente_id)

        estado = params.get('estado')
        if estado:
            qs = qs.filter(estado=estado)

        desde = params.get('desde')
        if desde:
            qs = qs.filter(fecha__gte=desde)

        hasta = params.get('hasta')
        if hasta:
            qs = qs.filter(fecha__lte=hasta)

        return qs
