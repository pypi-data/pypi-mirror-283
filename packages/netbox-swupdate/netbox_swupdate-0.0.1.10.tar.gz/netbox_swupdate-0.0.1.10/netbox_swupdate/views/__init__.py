from .view_deploy import DeployDeleteView, DeployEditView, DeployListView, DeployView
from .view_monitoring import (
    MonitoringDeleteView,
    MonitoringEditView,
    MonitoringListView,
    MonitoringView,
)
from .view_repository import (
    RepositoryDeleteView,
    RepositoryEditView,
    RepositoryListView,
    RepositoryView,
)
from .view_software import (
    SoftwareDeleteView,
    SoftwareEditView,
    SoftwareListView,
    SoftwareView,
)

__all__ = (
    "RepositoryListView",
    "RepositoryEditView",
    "RepositoryView",
    "RepositoryDeleteView",
    "DeployDeleteView",
    "DeployEditView",
    "DeployListView",
    "DeployView",
    "SoftwareDeleteView",
    "SoftwareEditView",
    "SoftwareListView",
    "SoftwareView",
    "MonitoringDeleteView",
    "MonitoringEditView",
    "MonitoringListView",
    "MonitoringView",
)
