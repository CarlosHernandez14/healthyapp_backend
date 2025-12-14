from rest_framework.routers import DefaultRouter
from .views import RegistroDiarioViewSet, PlanAlimenticioViewSet

router = DefaultRouter()
router.register(r'registros', RegistroDiarioViewSet, basename='registros')
router.register(r'plan', PlanAlimenticioViewSet, basename='plan')

urlpatterns = router.urls
