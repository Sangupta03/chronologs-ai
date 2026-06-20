from django.db.models import Count
from django.db.models.functions import TruncDay
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from .filters import IncidentFilter
from .models import Incident
from .serializers import IncidentSerializer


class IncidentListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = IncidentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = IncidentFilter

    def get_queryset(self):
        return Incident.objects.filter(
            log_file__user=self.request.user
        ).order_by("-created_at")


class IncidentStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Incident.objects.filter(log_file__user=request.user)

        severity_counts = dict(
            queryset.values_list("severity").annotate(count=Count("id"))
        )

        daily_counts = (
            queryset
            .annotate(day=TruncDay("created_at"))
            .values("day")
            .annotate(count=Count("id"))
            .order_by("day")
        )

        return Response(
            {
                "severity_counts": severity_counts,
                "incidents_over_time": [
                    {"date": d["day"].date().isoformat(), "count": d["count"]}
                    for d in daily_counts
                ],
            }
        )
