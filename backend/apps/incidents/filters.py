import django_filters

from .models import Incident


class IncidentFilter(django_filters.FilterSet):
    start_after = django_filters.IsoDateTimeFilter(field_name="start_time", lookup_expr="gte")
    start_before = django_filters.IsoDateTimeFilter(field_name="start_time", lookup_expr="lte")

    class Meta:
        model = Incident
        fields = ["severity", "log_file", "start_after", "start_before"]
