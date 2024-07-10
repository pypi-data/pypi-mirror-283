from django.urls import path
from netbox.views.generic import ObjectChangeLogView

from netbox_swupdate.models import Deploy
from netbox_swupdate.views import (
    DeployDeleteView,
    DeployEditView,
    DeployListView,
    DeployView,
)

urlpatterns = [
    path(
        "deployments/",
        DeployListView.as_view(),
        name="deploy_list",
    ),
    path(
        "deploy/add/",
        DeployEditView.as_view(),
        name="deploy_add",
    ),
    path(
        "deploy/<int:pk>/",
        DeployView.as_view(),
        name="deploy",
    ),
    path(
        "deploy/<int:pk>/edit/",
        DeployEditView.as_view(),
        name="deploy_edit",
    ),
    path(
        "deploy/<int:pk>/delete/",
        DeployDeleteView.as_view(),
        name="deploy_delete",
    ),
    path(
        "deploy/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="repository_changelog",
        kwargs={"model": Deploy},
    ),
]
