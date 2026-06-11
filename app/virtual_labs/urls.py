from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(
    r'virtual-labs', views.VirtualLabViewSet, basename='virtuallab',
    )
router.register(
    r'virtual-lab-labels', views.VirtualLabLabelViewSet,
    basename='virtuallablabel',
    )
