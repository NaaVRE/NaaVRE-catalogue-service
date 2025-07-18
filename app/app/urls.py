from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from django.conf import settings

from paas_configuration.urls import router as paas_configuration_router
from virtual_lab_instances.urls import router as virtual_lab_instances_router
from virtual_labs.urls import router as virtual_labs_router
from workflow_cells.urls import router as workflow_cells_router
from workflows.urls import router as workflows_router

router = DefaultRouter()
router.registry.extend(paas_configuration_router.registry)
router.registry.extend(virtual_lab_instances_router.registry)
router.registry.extend(virtual_labs_router.registry)
router.registry.extend(workflow_cells_router.registry)
router.registry.extend(workflows_router.registry)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include("rest_framework.urls", namespace="rest_framework")),
    path('', include(router.urls)),
    ]

if settings.BASE_PATH:
    urlpatterns = [
        path(f'{settings.BASE_PATH}/', include(urlpatterns)),
        path('', lambda request: redirect(f'{settings.BASE_PATH}/')),
        ]
