from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(
    r'virtual-lab-instances', views.VirtualLabInstanceViewSet,
    basename='virtual-lab-instance',
    )
