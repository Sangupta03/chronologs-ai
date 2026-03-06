

import uuid
from django.db import models
from apps.logs.models import LogFile


class Incident(models.Model):

    SEVERITY_LEVELS = [
        ("LOW", "Low"),
        ("MEDIUM", "Medium"),
        ("HIGH", "High"),
        ("CRITICAL", "Critical"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    log_file = models.ForeignKey(
        LogFile,
        on_delete=models.CASCADE,
        related_name="incidents"
    )

    title = models.CharField(max_length=255)

    severity = models.CharField(
        max_length=10,
        choices=SEVERITY_LEVELS
    )

    severity_score = models.FloatField()

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    event_count = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.severity})"
