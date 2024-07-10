from django.db.models import Q
from netbox.filtersets import NetBoxModelFilterSet

from netbox_swupdate.models import Monitoring

__all__ = ("MonitoringFilterSet",)


class MonitoringFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = Monitoring
        fields = ("id", "device", "status", "update_time")

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = (
            Q(status__icontains=value)
            | Q(update_time__icontains=value)
            | Q(device__name__icontains=value)
        )
        return queryset.filter(qs_filter).distinct()
