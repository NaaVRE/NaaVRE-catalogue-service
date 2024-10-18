from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from virtual_labs.urls import router as virtual_labs_router
from workflow_cells.urls import router as workflow_cells_router
from workflows.urls import router as workflows_router

router = DefaultRouter()
router.registry.extend(virtual_labs_router.registry)
router.registry.extend(workflow_cells_router.registry)
router.registry.extend(workflows_router.registry)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include("rest_framework.urls", namespace="rest_framework")),
    path('', include(router.urls)),
    ]
