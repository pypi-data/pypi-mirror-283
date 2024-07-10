from django.urls import include, path
from netbox.api.routers import NetBoxRouter

from netbox_swupdate.api.views import (
    DeployViewSet,
    MonitoringViewSet,
    RepositoryViewSet,
    SoftwareViewSet,
)

router = NetBoxRouter()
router.register("repository", RepositoryViewSet)
router.register("deploy", DeployViewSet)
router.register("monitoring", MonitoringViewSet)
router.register("software", SoftwareViewSet)
urlpatterns = [
    path("", include(router.urls)),
]
