from django.urls import include, path
from netbox.api.routers import NetBoxRouter

from netbox_swupdate.api.views import RepositoryViewSet

router = NetBoxRouter()
router.register("repository", RepositoryViewSet)
urlpatterns = [
    path("", include(router.urls)),
]
