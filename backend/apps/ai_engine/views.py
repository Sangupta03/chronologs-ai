from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.logs.models import LogEvent, LogFile
from .vectorizer import vectorize_logs
from .clustering import cluster_logs

from .anomaly import detect_anomalies
from .incident_engine import create_incidents
class AnalyzeLogsView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, log_file_id):

        # 1️⃣ Get LogFile
        try:
            log_file = LogFile.objects.get(id=log_file_id, user=request.user)
        except LogFile.DoesNotExist:
            return Response({"error": "Log file not found"}, status=404)

        # 2️⃣ Fetch events
        events = LogEvent.objects.filter(log_file=log_file)

        if not events.exists():
            return Response({"error": "No events found"}, status=400)

        # 3️⃣ Extract messages
        messages = [event.message for event in events]

        # 4️⃣ Vectorize
        vectors, _ = vectorize_logs(messages)

        # 5️⃣ Cluster
        k = max(1, min(2, len(messages)//2))
        labels, _ = cluster_logs(vectors, k = k)

        # 6️⃣ Detect anomalies
        anomalies, _ = detect_anomalies(vectors)

        # 7️⃣ Save cluster_id + anomaly
        for event, label, anomaly in zip(events, labels, anomalies):
            event.cluster_id = int(label)
            event.is_anomaly = bool(anomaly)

        LogEvent.objects.bulk_update(events, ["cluster_id", "is_anomaly"])

        # 8️⃣ Refresh events from DB
        events = LogEvent.objects.filter(log_file=log_file)

        # 9️⃣ Create incidents
        incident_count = create_incidents(log_file, events)

        # Prepare response
        cluster_counts = {}
        for label in labels:
            label = int(label)
            cluster_counts[label] = cluster_counts.get(label, 0) + 1

        return Response({
            "status": "analysis completed",
            "total_events": len(messages),
            "clusters": cluster_counts,
            "incidents_created": incident_count
        })