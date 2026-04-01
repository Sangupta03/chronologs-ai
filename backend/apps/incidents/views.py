
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Incident


class IncidentListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        incidents = Incident.objects.all().order_by("-created_at")

        data = [
            {
                "id": str(i.id),
                "title": i.title,
                "severity": i.severity,
                "start_time": i.start_time,
                "end_time": i.end_time,
                "event_count": i.event_count,
                "summary": i.summary,
            }
            for i in incidents
        ]

        return Response(data)