#from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import LogFile
from .serializers import LogUploadSerializer
from .tasks import process_log_file


class LogUploadView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = LogUploadSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        uploaded_file = serializer.validated_data["file"]

        log_file = LogFile.objects.create(
            user=request.user,
            file=uploaded_file,
            file_name=uploaded_file.name,
            file_size=uploaded_file.size,
            status="processing"
        )

        process_log_file.delay(str(log_file.id))

        return Response(
            {
                "log_file_id": str(log_file.id),
                "file_name": log_file.file_name,
                "status": log_file.status,
            },
            status=status.HTTP_202_ACCEPTED,
        )


class LogFileStatusView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, log_file_id):
        try:
            log_file = LogFile.objects.get(id=log_file_id, user=request.user)
        except LogFile.DoesNotExist:
            return Response({"error": "Log file not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response(
            {
                "log_file_id": str(log_file.id),
                "file_name": log_file.file_name,
                "status": log_file.status,
                "total_events": log_file.total_events,
                "events_parsed": log_file.events_parsed,
                "events_failed": log_file.events_failed,
                "processing_time_seconds": log_file.processing_time,
            }
        )