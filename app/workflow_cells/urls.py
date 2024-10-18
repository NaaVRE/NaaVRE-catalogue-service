from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'workflow-cells', views.CellViewSet, basename='cell')
