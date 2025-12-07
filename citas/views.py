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
    queryset = Cita.objects.all().order_by('id')
    serializer_class = CitaSerializer
    pagination_class = CitaPagination
    permission_classes = [IsAuthenticated]

    # Filtros simples por paciente
    def get_queryset(self):
        qs = super().get_queryset()
        paciente_id = self.request.query_params.get('paciente')
        if paciente_id:
            qs = qs.filter(paciente_id=paciente_id)
        return qs
