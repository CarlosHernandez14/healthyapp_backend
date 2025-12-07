from rest_framework.routers import DefaultRouter
from .views import CitaViewSet

router = DefaultRouter()
router.register(r'citas', CitaViewSet, basename='citas')

urlpatterns = router.urls
