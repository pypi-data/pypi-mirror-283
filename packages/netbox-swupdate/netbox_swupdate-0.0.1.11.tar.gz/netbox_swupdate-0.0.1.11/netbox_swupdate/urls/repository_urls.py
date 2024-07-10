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
        "repositories/",
        RepositoryListView.as_view(),
        name="repository_list",
    ),
    path(
        "repository/add/",
        RepositoryEditView.as_view(),
        name="repository_add",
    ),
    path(
        "repository/<int:pk>/",
        RepositoryView.as_view(),
        name="repository",
    ),
    path(
        "repository/<int:pk>/edit/",
        RepositoryEditView.as_view(),
        name="repository_edit",
    ),
    path(
        "repository/<int:pk>/delete/",
        RepositoryDeleteView.as_view(),
        name="repository_delete",
    ),
    path(
        "repository/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="repository_changelog",
        kwargs={"model": Repository},
    ),
]
