from rest_framework.routers import DefaultRouter
from .views import RegistroDiarioViewSet

router = DefaultRouter()
router.register(r'registros', RegistroDiarioViewSet, basename='registros')

urlpatterns = router.urls