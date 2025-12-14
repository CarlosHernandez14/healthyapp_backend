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

    # Filtros por paciente, estado, tipo y rango de fechas (acepta alias del UI)
    def get_queryset(self):
        qs = super().get_queryset()
        params = self.request.query_params

        # Aceptar alias de parámetros desde el UI
        paciente_id = params.get('paciente') or params.get('paciente_id')
        estado = params.get('estado')
        tipo = params.get('tipo')
        # Soporta 'date_from'/'date_to' y también 'fecha_inicio'/'fecha_fin' (u otros alias comunes)
        date_from = params.get('date_from') or params.get('fecha_inicio') or params.get('fecha_desde') or params.get('from')
        date_to = params.get('date_to') or params.get('fecha_fin') or params.get('fecha_hasta') or params.get('to')

        if paciente_id:
            qs = qs.filter(paciente_id=paciente_id)

        if estado:
            e = (estado or '').strip().casefold()
            estado_map = {
                'pendiente': 'pendiente',
                'asistida': 'asistida',
                'asistido': 'asistida',
                'cancelada': 'cancelada',
                'cancelado': 'cancelada',
            }
            if e in estado_map:
                qs = qs.filter(estado=estado_map[e])
            else:
                # fallback a comparación case-insensitive directa
                qs = qs.filter(estado__iexact=estado)

        if tipo:
            t_raw = (tipo or '').strip()
            # If the UI encodes spaces as '+', normalize them back to spaces
            t = t_raw.replace('+', ' ').casefold()
            tipo_map = {
                'primera': 'primera',
                'primera vez': 'primera',
                'first': 'primera',
                'first time': 'primera',
                'seguimiento': 'seguimiento',
                'followup': 'seguimiento',
                'follow-up': 'seguimiento',
                'follow up': 'seguimiento',
            }
            if t in tipo_map:
                qs = qs.filter(tipo=tipo_map[t])
            else:
                # heurística por inclusión del término
                if 'primera' in t or 'first' in t:
                    qs = qs.filter(tipo='primera')
                elif 'seguim' in t or 'follow' in t:
                    qs = qs.filter(tipo='seguimiento')
                else:
                    qs = qs.filter(tipo__iexact=tipo)

        # Normalize possible datetime inputs like 'YYYY-MM-DDTHH:mm:ssZ' or with slashes/spaces
        def _norm_date(s):
            if not s:
                return None
            v = (s or '').strip().replace('/', '-')
            if 'T' in v:
                v = v.split('T', 1)[0]
            if ' ' in v:
                v = v.split(' ', 1)[0]
            return v

        date_from_n = _norm_date(date_from)
        date_to_n = _norm_date(date_to)

        if date_from_n:
            qs = qs.filter(fecha__gte=date_from_n)
        if date_to_n:
            qs = qs.filter(fecha__lte=date_to_n)

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
