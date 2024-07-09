from django.urls import path
from views import (
    RepositoryCreateView,
    RepositoryDeleteView,
    RepositoryDetailView,
    RepositoryListView,
    RepositoryUpdateView,
)

urlpatterns = [
    path(
        "swupdate/repository/",
        RepositoryListView.as_view(),
        name="repository_list",
    ),
    path(
        "swupdate/repository/add/",
        RepositoryCreateView.as_view(),
        name="repository_add",
    ),
    path(
        "swupdate/repository/<int:pk>/",
        RepositoryDetailView.as_view(),
        name="repository_detail",
    ),
    path(
        "swupdate/repository/<int:pk>/edit/",
        RepositoryUpdateView.as_view(),
        name="repository_edit",
    ),
    path(
        "swupdate/repository/<int:pk>/delete/",
        RepositoryDeleteView.as_view(),
        name="repository_delete",
    ),
]
