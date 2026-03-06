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