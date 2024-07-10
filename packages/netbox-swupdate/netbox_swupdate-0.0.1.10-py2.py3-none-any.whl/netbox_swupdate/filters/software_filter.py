from django.db.models import Q
from netbox.filtersets import NetBoxModelFilterSet

from netbox_swupdate.models import Software

__all__ = ("SoftwareFilterSet",)


class SoftwareFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = Software
        fields = ("id", "name", "version", "description", "creation_date")

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = Q(name__icontains=value) | Q(version__icontains=value)
        return queryset.filter(qs_filter).distinct()
