from netbox.views import generic

from netbox_swupdate.models import Repository

__all__ = (
    "RepositoryListView",
    "RepositoryCreateView",
    "RepositoryDetailView",
    "RepositoryUpdateView",
    "RepositoryDeleteView",
)


class RepositoryListView(generic.ObjectListView):
    model = Repository
    template_name = "netbox_swupdate/repository_list.html"


class RepositoryCreateView(generic.ObjectView):
    model = Repository
    template_name = "netbox_swupdate/repository_form.html"
    fields = "__all__"


class RepositoryDetailView(generic.ObjectView):
    model = Repository
    template_name = "netbox_swupdate/repository_detail.html"


class RepositoryUpdateView(generic.ObjectEditView):
    model = Repository
    template_name = "netbox_swupdate/repository_form.html"
    fields = "__all__"


class RepositoryDeleteView(generic.ObjectDeleteView):
    model = Repository
    template_name = "netbox_swupdate/repository_confirm_delete.html"
    success_url = "/swupdate/repository/"
