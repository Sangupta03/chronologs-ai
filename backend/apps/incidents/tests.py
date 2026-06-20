from datetime import datetime

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from apps.logs.models import LogFile
from .models import Incident

User = get_user_model()


def make_incident(log_file, severity, title="Incident"):
    return Incident.objects.create(
        log_file=log_file,
        title=title,
        severity=severity,
        severity_score=0.5,
        start_time=datetime(2026, 1, 1, 12, 0, 0),
        end_time=datetime(2026, 1, 1, 12, 5, 0),
        event_count=1,
    )


class IncidentListTests(APITestCase):
    def setUp(self):
        self.user_a = User.objects.create_user(email="a@example.com", password="Str0ngPassword!9")
        self.user_b = User.objects.create_user(email="b@example.com", password="Str0ngPassword!9")

        self.log_file_a = LogFile.objects.create(
            user=self.user_a, file_name="a.log", file_size=1, status="completed"
        )
        self.log_file_b = LogFile.objects.create(
            user=self.user_b, file_name="b.log", file_size=1, status="completed"
        )

        for _ in range(12):
            make_incident(self.log_file_a, "LOW")
        make_incident(self.log_file_a, "CRITICAL", title="Critical one")
        make_incident(self.log_file_b, "CRITICAL", title="Belongs to user B")

        self.client.force_authenticate(user=self.user_a)

    def test_user_only_sees_their_own_incidents(self):
        res = self.client.get("/api/incidents/")
        self.assertEqual(res.status_code, 200)
        returned_log_files = {i["log_file"] for i in res.data["results"]}
        self.assertNotIn(str(self.log_file_b.id), returned_log_files)

    def test_pagination_limits_page_size(self):
        res = self.client.get("/api/incidents/")
        self.assertEqual(res.data["count"], 13)
        self.assertEqual(len(res.data["results"]), 10)  # PAGE_SIZE
        self.assertIsNotNone(res.data["next"])

    def test_severity_filter(self):
        res = self.client.get("/api/incidents/", {"severity": "CRITICAL"})
        self.assertEqual(res.data["count"], 1)
        self.assertEqual(res.data["results"][0]["title"], "Critical one")
