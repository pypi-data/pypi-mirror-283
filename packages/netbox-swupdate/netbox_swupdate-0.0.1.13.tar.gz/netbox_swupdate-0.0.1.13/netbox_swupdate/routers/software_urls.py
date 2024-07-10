from django.urls import path
from netbox.views.generic import ObjectChangeLogView

from netbox_swupdate.models import Software
from netbox_swupdate.views import (
    SoftwareDeleteView,
    SoftwareEditView,
    SoftwareListView,
    SoftwareView,
)

urlpatterns = [
    path(
        "softwares/",
        SoftwareListView.as_view(),
        name="software_list",
    ),
    path(
        "software/add/",
        SoftwareEditView.as_view(),
        name="software_add",
    ),
    path(
        "software/<int:pk>/",
        SoftwareView.as_view(),
        name="software",
    ),
    path(
        "software/<int:pk>/edit/",
        SoftwareEditView.as_view(),
        name="software_edit",
    ),
    path(
        "software/<int:pk>/delete/",
        SoftwareDeleteView.as_view(),
        name="software_delete",
    ),
    path(
        "software/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="software_changelog",
        kwargs={"model": Software},
    ),
]
