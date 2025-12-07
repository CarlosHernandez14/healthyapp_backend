from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from .models import RegistroDiario
from .serializers import RegistroDiarioSerializer

class RegistroDiarioPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class RegistroDiarioViewSet(viewsets.ModelViewSet):
    queryset = RegistroDiario.objects.all().order_by('-fecha')
    serializer_class = RegistroDiarioSerializer
    pagination_class = RegistroDiarioPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['observaciones', 'cita__motivo', 'cita__paciente__nombre', 'cita__paciente__apellido']
    ordering_fields = ['id', 'fecha', 'cumplio']
    ordering = ['-fecha']

    def get_queryset(self):
        qs = super().get_queryset()
        params = self.request.query_params

        cita_id = params.get('cita')
        paciente_id = params.get('paciente')
        cumplio = params.get('cumplio')  # 'true' | 'false'
        date_from = params.get('date_from')
        date_to = params.get('date_to')

        if cita_id:
            qs = qs.filter(cita_id=cita_id)
        if paciente_id:
            qs = qs.filter(cita__paciente_id=paciente_id)
        if cumplio is not None:
            if cumplio.lower() in ['true', '1', 'yes', 'si']:
                qs = qs.filter(cumplio=True)
            elif cumplio.lower() in ['false', '0', 'no']:
                qs = qs.filter(cumplio=False)
        if date_from:
            qs = qs.filter(fecha__gte=date_from)
        if date_to:
            qs = qs.filter(fecha__lte=date_to)

        return qs
