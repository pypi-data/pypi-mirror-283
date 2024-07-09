from netbox.api.routers import NetBoxRouter

from netbox_swupdate.api.views import RepositoryViewSet

router = NetBoxRouter()
router.register("repository", RepositoryViewSet)
urlpatterns = router.urls
