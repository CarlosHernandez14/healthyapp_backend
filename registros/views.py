from rest_framework import viewsets
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

    def get_queryset(self):
        qs = super().get_queryset()
        params = self.request.query_params

        cita_id = params.get('cita')
        if cita_id:
            qs = qs.filter(cita_id=cita_id)

        desde = params.get('desde')
        if desde:
            qs = qs.filter(fecha__gte=desde)

        hasta = params.get('hasta')
        if hasta:
            qs = qs.filter(fecha__lte=hasta)

        return qs
