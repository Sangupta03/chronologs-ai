from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.logs.models import LogEvent, LogFile
from .embeddings import search_index
from .tasks import analyze_log_file


class AnalyzeLogsView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, log_file_id):

        try:
            log_file = LogFile.objects.get(id=log_file_id, user=request.user)
        except LogFile.DoesNotExist:
            return Response({"error": "Log file not found"}, status=404)

        analyze_log_file.delay(str(log_file.id))

        return Response(
            {"log_file_id": str(log_file.id), "status": "analyzing"},
            status=202,
        )


class AnalysisStatusView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, log_file_id):
        try:
            log_file = LogFile.objects.get(id=log_file_id, user=request.user)
        except LogFile.DoesNotExist:
            return Response({"error": "Log file not found"}, status=404)

        return Response(
            {
                "log_file_id": str(log_file.id),
                "status": log_file.status,
                "result": log_file.analysis_result,
                "error": log_file.analysis_error,
            }
        )


class SemanticSearchView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, log_file_id):
        try:
            log_file = LogFile.objects.get(id=log_file_id, user=request.user)
        except LogFile.DoesNotExist:
            return Response({"error": "Log file not found"}, status=404)

        query = request.query_params.get("q", "").strip()
        if not query:
            return Response({"error": "Missing query parameter 'q'"}, status=400)

        matches = search_index(str(log_file.id), query, top_k=10)
        if matches is None:
            return Response(
                {"error": "No search index available for this log file yet"},
                status=400,
            )

        events_by_id = {
            str(e.id): e
            for e in LogEvent.objects.filter(
                log_file=log_file, id__in=[m[0] for m in matches]
            )
        }

        results = [
            {
                "event_id": event_id,
                "distance": distance,
                "timestamp": events_by_id[event_id].timestamp,
                "log_level": events_by_id[event_id].log_level,
                "service_name": events_by_id[event_id].service_name,
                "message": events_by_id[event_id].message,
            }
            for event_id, distance in matches
            if event_id in events_by_id
        ]

        return Response({"query": query, "results": results})