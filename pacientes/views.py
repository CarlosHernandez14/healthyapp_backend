from django.shortcuts import render

from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from .models import Paciente
from .serializers import PacienteSerializer
from rest_framework.permissions import IsAuthenticated


class PacientePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all().order_by('id')
    serializer_class = PacienteSerializer
    pagination_class = PacientePagination
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'apellido']
    ordering_fields = ['id', 'nombre', 'apellido']

    # Filtro adicional por género (?genero=M|F|...)
    def get_queryset(self):
        qs = super().get_queryset()
        genero = self.request.query_params.get('genero')
        if genero:
            qs = qs.filter(genero=genero)
        return qs
