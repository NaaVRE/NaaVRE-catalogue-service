from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(
    r'sharing-scopes', views.SharingScopeViewset, basename='sharingscope',
    )
