from django.urls import include, path

urlpatterns = [
    path("", include("netbox_swupdate.urls.monitoring_urls")),
    path("", include("netbox_swupdate.urls.software_urls")),
    path("", include("netbox_swupdate.urls.repository_urls")),
    path("", include("netbox_swupdate.urls.deploy_urls")),
]
