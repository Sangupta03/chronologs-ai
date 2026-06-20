from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.logs.models import LogEvent, LogFile
from .incident_engine import create_incidents
from .pipeline import compute_k
from .storytelling import extract_incident_facts, render_rule_based_summary

User = get_user_model()


class ComputeKTests(TestCase):
    def test_small_dataset_uses_one_cluster(self):
        self.assertEqual(compute_k(5), 1)

    def test_scales_with_dataset_size(self):
        self.assertEqual(compute_k(30), 2)
        self.assertEqual(compute_k(75), 5)

    def test_caps_at_eight_clusters(self):
        self.assertEqual(compute_k(10000), 8)


class IncidentSeverityTests(TestCase):
    """
    Regression test for the bug where severity_score double-counted
    events that were both an ERROR and an anomaly, inflating the score
    above 1.0. It must now be the fraction of *unique* flagged events.
    """

    def setUp(self):
        user = User.objects.create_user(email="severity@example.com", password="Testpass123!")
        self.log_file = LogFile.objects.create(
            user=user, file_name="x.log", file_size=10, status="clustered"
        )

    def _make_event(self, level, is_anomaly, cluster_id=0):
        return LogEvent.objects.create(
            log_file=self.log_file,
            timestamp=datetime(2026, 1, 1, 12, 0, 0),
            log_level=level,
            service_name="svc",
            message="Database connection timeout",
            raw_log="raw",
            event_hash="hash",
            cluster_id=cluster_id,
            is_anomaly=is_anomaly,
        )

    def test_severity_score_never_exceeds_one(self):
        # 4 events, all both ERROR and anomaly: naive double-counting would
        # give (4 + 4) / 4 = 2.0; the fix should cap it at 1.0.
        events = [self._make_event("ERROR", True) for _ in range(4)]

        create_incidents(self.log_file, LogEvent.objects.filter(log_file=self.log_file))

        from apps.incidents.models import Incident
        incident = Incident.objects.get(log_file=self.log_file)
        self.assertEqual(incident.severity_score, 1.0)
        self.assertEqual(incident.severity, "CRITICAL")

    def test_events_are_linked_to_their_incident(self):
        for _ in range(3):
            self._make_event("ERROR", False)

        create_incidents(self.log_file, LogEvent.objects.filter(log_file=self.log_file))

        events = LogEvent.objects.filter(log_file=self.log_file)
        self.assertTrue(all(e.incident_id is not None for e in events))


class StorytellingTests(TestCase):
    def test_extract_incident_facts_returns_none_for_empty_events(self):
        self.assertIsNone(extract_incident_facts([]))

    def test_render_rule_based_summary_handles_no_facts(self):
        self.assertEqual(
            render_rule_based_summary(None),
            "No events available for this incident.",
        )

    def test_render_rule_based_summary_includes_key_facts(self):
        class FakeEvent:
            def __init__(self, level, service, message, ts):
                self.log_level = level
                self.service_name = service
                self.message = message
                self.timestamp = ts
                self.is_anomaly = False

        base = datetime(2026, 1, 1, 12, 0, 0)
        events = [
            FakeEvent("ERROR", "payment-service", "Database connection timeout", base),
            FakeEvent("ERROR", "payment-service", "Database connection timeout", base + timedelta(seconds=1)),
            FakeEvent("INFO", "payment-service", "Retry succeeded", base + timedelta(seconds=2)),
        ]

        facts = extract_incident_facts(events)
        summary = render_rule_based_summary(facts)

        self.assertIn("payment-service", summary)
        self.assertIn("Database connection timeout", summary)
