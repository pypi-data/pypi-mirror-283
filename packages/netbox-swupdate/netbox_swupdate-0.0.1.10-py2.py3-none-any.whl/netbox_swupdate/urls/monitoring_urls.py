from django.urls import path
from netbox.views.generic import ObjectChangeLogView

from netbox_swupdate.models import Monitoring
from netbox_swupdate.views import (
    MonitoringDeleteView,
    MonitoringEditView,
    MonitoringListView,
    MonitoringView,
)

urlpatterns = [
    path(
        "monitorings/",
        MonitoringListView.as_view(),
        name="monitoring_list",
    ),
    path(
        "monitoring/add/",
        MonitoringEditView.as_view(),
        name="monitoring_add",
    ),
    path(
        "monitoring/<int:pk>/",
        MonitoringView.as_view(),
        name="monitoring",
    ),
    path(
        "monitoring/<int:pk>/edit/",
        MonitoringEditView.as_view(),
        name="monitoring_edit",
    ),
    path(
        "monitoring/<int:pk>/delete/",
        MonitoringDeleteView.as_view(),
        name="monitoring_delete",
    ),
    path(
        "monitoring/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="monitoring_changelog",
        kwargs={"model": Monitoring},
    ),
]
