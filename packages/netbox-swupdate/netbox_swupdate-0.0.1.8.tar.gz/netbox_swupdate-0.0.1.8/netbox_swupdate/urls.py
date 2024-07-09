from django.urls import path
from netbox.views.generic import ObjectChangeLogView

from netbox_swupdate.models import Repository
from netbox_swupdate.views import (
    RepositoryDeleteView,
    RepositoryEditView,
    RepositoryListView,
    RepositoryView,
)

urlpatterns = [
    path(
        "swupdate/repository/",
        RepositoryListView.as_view(),
        name="repository_list",
    ),
    path(
        "swupdate/repository/add/",
        RepositoryEditView,
        name="repository_add",
    ),
    path(
        "swupdate/repository/<int:pk>/",
        RepositoryView.as_view(),
        name="repository_detail",
    ),
    path(
        "swupdate/repository/<int:pk>/edit/",
        RepositoryEditView.as_view(),
        name="repository_edit",
    ),
    path(
        "swupdate/repository/<int:pk>/delete/",
        RepositoryDeleteView.as_view(),
        name="repository_delete",
    ),
    path(
        "swupdate/repository/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="repository_changelog",
        kwargs={"model": Repository},
    ),
]
