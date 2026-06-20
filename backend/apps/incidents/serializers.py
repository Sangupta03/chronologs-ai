from rest_framework import serializers

from .models import Incident


class IncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident
        fields = [
            "id",
            "log_file",
            "title",
            "severity",
            "severity_score",
            "start_time",
            "end_time",
            "event_count",
            "created_at",
            "summary",
        ]
