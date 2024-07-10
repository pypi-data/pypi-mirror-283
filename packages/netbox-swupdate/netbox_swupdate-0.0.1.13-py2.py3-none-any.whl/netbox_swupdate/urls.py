from django.urls import include, path

urlpatterns = [
    path("", include("netbox_swupdate.routers.monitoring_urls")),
    path("", include("netbox_swupdate.routers.software_urls")),
    path("", include("netbox_swupdate.routers.repository_urls")),
    path("", include("netbox_swupdate.routers.deploy_urls")),
]
