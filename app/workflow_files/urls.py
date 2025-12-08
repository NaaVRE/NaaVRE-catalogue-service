from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'workflow-files', views.WorkflowFileViewSet, basename='workflowfile')
