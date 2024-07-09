from netbox.api.viewsets import NetBoxModelViewSet
from netbox.views import generic

from netbox_swupdate.filters import RepositoryFilterSet
from netbox_swupdate.forms import RepositoryForm
from netbox_swupdate.models import Repository
from netbox_swupdate.serializers import RepositorySerializer
from netbox_swupdate.tables import RepositoryTable

__all__ = (
    "RepositoryListView",
    "RepositoryView",
    "RepositoryEditView",
    "RepositoryDeleteView",
    "RepositoryViewSet",
)


class RepositoryListView(generic.ObjectListView):
    queryset = Repository.objects.all()
    filterset = RepositoryFilterSet
    table = RepositoryTable


class RepositoryEditView(generic.ObjectEditView):
    queryset = Repository.objects.all()
    form = RepositoryForm


class RepositoryView(generic.ObjectView):
    queryset = Repository.objects.all()


class RepositoryViewSet(NetBoxModelViewSet):
    queryset = Repository.objects.prefetch_related("tags")
    serializer_class = RepositorySerializer


class RepositoryDeleteView(generic.ObjectDeleteView):
    queryset = Repository.objects.all()
