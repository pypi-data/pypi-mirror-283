from django.db.models import Q
from netbox.filtersets import NetBoxModelFilterSet

from netbox_swupdate.models import Deploy

__all__ = ("DeployFilterSet",)


class DeployFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = Deploy
        fields = ("id", "name", "type")

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = Q(name__icontains=value) | Q(type__icontains=value)
        return queryset.filter(qs_filter).distinct()
