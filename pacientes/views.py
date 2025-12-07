from django.shortcuts import render

from rest_framework import viewsets
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
