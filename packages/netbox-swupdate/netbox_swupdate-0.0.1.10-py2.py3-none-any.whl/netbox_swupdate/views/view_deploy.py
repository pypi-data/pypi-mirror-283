from netbox.views import generic

from netbox_swupdate.filters import DeployFilterSet
from netbox_swupdate.forms import DeployForm
from netbox_swupdate.models import Deploy
from netbox_swupdate.tables import DeployTable

__all__ = (
    "DeployListView",
    "DeployView",
    "DeployEditView",
    "DeployDeleteView",
)


class DeployListView(generic.ObjectListView):
    queryset = Deploy.objects.all()
    filterset = DeployFilterSet
    table = DeployTable


class DeployEditView(generic.ObjectEditView):
    queryset = Deploy.objects.all()
    form = DeployForm


class DeployView(generic.ObjectView):
    queryset = Deploy.objects.all()


class DeployDeleteView(generic.ObjectDeleteView):
    queryset = Deploy.objects.all()
