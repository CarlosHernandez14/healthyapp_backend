from django.shortcuts import render

from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from .models import Cita
from .serializers import CitaSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

class CitaPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class CitaViewSet(viewsets.ModelViewSet):
    queryset = Cita.objects.all().order_by('id')
    serializer_class = CitaSerializer
    pagination_class = CitaPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['motivo', 'paciente__nombre', 'paciente__apellido']
    ordering_fields = ['id', 'fecha', 'hora', 'estado', 'tipo']
    ordering = ['-fecha', '-hora']

    # Filtros por paciente, estado, tipo y rango de fechas (date_from, date_to)
    def get_queryset(self):
        qs = super().get_queryset()
        params = self.request.query_params

        paciente_id = params.get('paciente')
        estado = params.get('estado')
        tipo = params.get('tipo')
        date_from = params.get('date_from')
        date_to = params.get('date_to')

        if paciente_id:
            qs = qs.filter(paciente_id=paciente_id)
        if estado:
            qs = qs.filter(estado=estado)
        if tipo:
            qs = qs.filter(tipo=tipo)
        if date_from:
            qs = qs.filter(fecha__gte=date_from)
        if date_to:
            qs = qs.filter(fecha__lte=date_to)

        return qs

    @action(detail=True, methods=['post'])
    def cancelar(self, request, pk=None):
        """
        Marca la cita como cancelada.
        """
        cita = self.get_object()
        if cita.estado == 'cancelada':
            return Response({'detail': 'La cita ya está cancelada.'}, status=status.HTTP_400_BAD_REQUEST)
        cita.estado = 'cancelada'
        cita.save()
        return Response(self.get_serializer(cita).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def asistir(self, request, pk=None):
        """
        Marca la cita como asistida.
        """
        cita = self.get_object()
        if cita.estado == 'asistida':
            return Response({'detail': 'La cita ya fue marcada como asistida.'}, status=status.HTTP_400_BAD_REQUEST)
        cita.estado = 'asistida'
        cita.save()
        return Response(self.get_serializer(cita).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def meta(self, request):
        """
        Devuelve los catálogos de la entidad (opciones de estado y tipo) para poblar selects en el UI.
        """
        estados = [{'value': key, 'label': label} for key, label in Cita.ESTADOS]
        tipos = [{'value': key, 'label': label} for key, label in Cita.TIPOS]
        return Response({'estados': estados, 'tipos': tipos})
