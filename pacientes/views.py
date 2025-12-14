from django.shortcuts import render

from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from .models import Paciente
from .serializers import PacienteSerializer
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.db.models.functions import Lower, Trim


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
    ordering = ['nombre', 'apellido']

    def get_queryset(self):
        qs = super().get_queryset()
        params = self.request.query_params

        genero = params.get('genero')
        min_edad = params.get('min_edad')
        max_edad = params.get('max_edad')

        if genero:
            norm = (genero or '').strip().casefold()
            male_aliases = {'m', 'masculino', 'masc', 'male', 'h', 'hombre'}
            female_aliases = {'f', 'femenino', 'fem', 'female', 'mujer'}
            # Normalize DB values (trim + lowercase) and then compare against canonical set
            qs = qs.annotate(_genero_norm=Lower(Trim('genero')))
            if norm in male_aliases:
                qs = qs.filter(_genero_norm__in=['masculino', 'm'])
            elif norm in female_aliases:
                qs = qs.filter(_genero_norm__in=['femenino', 'f'])
            else:
                # Fallback: compare normalized value directly
                qs = qs.filter(_genero_norm=norm)
        if min_edad:
            qs = qs.filter(edad__gte=min_edad)
        if max_edad:
            qs = qs.filter(edad__lte=max_edad)

        return qs
