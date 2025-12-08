from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'notebook-files', views.NotebookFileViewSet, basename='notebookfile')
