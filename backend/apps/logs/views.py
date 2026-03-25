#from django.shortcuts import render

# Create your views here.
import time
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import LogFile, LogEvent
from .serializers import LogUploadSerializer
from .parser import parse_log_file


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

        start_time = time.time()

        events_parsed, events_failed = parse_log_file(log_file)

        processing_time = round(time.time() - start_time, 2)

        log_file.status = "parsed"
        log_file.total_events = events_parsed
        log_file.events_parsed = events_parsed
        log_file.events_failed = events_failed
        log_file.processing_time = processing_time

        log_file.save()

        return Response(
            {
                "log_file_id": str(log_file.id),
                "file_name": log_file.file_name,
                "status": log_file.status,
                "events_parsed": events_parsed,
                "events_failed": events_failed,
                "processing_time_seconds": processing_time,
            }
        )