from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(
    r'paas-configuration', views.PaasConfigurationViewSet,
    )
