# Create your models here.
import uuid
from django.db import models
from django.conf import settings


class LogFile(models.Model):

    STATUS_CHOICES = [
        ("uploaded", "Uploaded"),
        ("processing", "Processing"),
        ("parsed", "Parsed"),
        ("clustered", "Clustered"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="log_files"
    )
    
    file = models.FileField(upload_to="logs/", null=True, blank=True)

    file_name = models.CharField(max_length=255)

    file_size = models.IntegerField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="uploaded"
    )

    upload_time = models.DateTimeField(auto_now_add=True)

    processing_started_at = models.DateTimeField(null=True, blank=True)

    processing_finished_at = models.DateTimeField(null=True, blank=True)

    total_events = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.file_name} ({self.status})"
    
class LogEvent(models.Model):

    LOG_LEVELS = [
        ("DEBUG", "Debug"),
        ("INFO", "Info"),
        ("WARN", "Warning"),
        ("ERROR", "Error"),
        ("CRITICAL", "Critical"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    log_file = models.ForeignKey(
        LogFile,
        on_delete=models.CASCADE,
        related_name="events"
    )

    timestamp = models.DateTimeField()

    log_level = models.CharField(
        max_length=10,
        choices=LOG_LEVELS
    )

    service_name = models.CharField(max_length=100)

    message = models.TextField()

    raw_log = models.TextField()

    event_hash = models.CharField(max_length=64)

    is_anomaly = models.BooleanField(default=False)

    incident = models.ForeignKey(
        "incidents.Incident",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="events"
    )

    class Meta:
        indexes = [
            models.Index(fields=["timestamp"]),
            models.Index(fields=["log_level"]),
            models.Index(fields=["service_name"]),
        ]

    def __str__(self):
        return f"{self.log_level} - {self.service_name}"