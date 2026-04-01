from collections import defaultdict

from apps.incidents.models import Incident
from .storytelling import generate_incident_summary


def create_incidents(log_file, events):
    Incident.objects.filter(log_file=log_file).delete()

    cluster_groups = defaultdict(list)

    # Group events by cluster
    for event in events:
        cluster_groups[event.cluster_id].append(event)

    incidents_created = 0

    for cluster_id, cluster_events in cluster_groups.items():

        error_count = sum(
            1 for e in cluster_events if e.log_level.strip().upper() == "ERROR"
        )
        anomaly_count = sum(1 for e in cluster_events if e.is_anomaly)

        # Rule for incident creation
        if error_count == 0 and anomaly_count == 0:
            continue

        if len(cluster_events) < 2 and error_count < 2:
            continue

        # ✅ NOW THIS RUNS (correct indentation)
        start_time = min(e.timestamp for e in cluster_events)
        end_time = max(e.timestamp for e in cluster_events)

        severity_score = (error_count + anomaly_count) / len(cluster_events)

        if severity_score > 0.7:
            severity = "CRITICAL"
        elif severity_score > 0.4:
            severity = "HIGH"
        elif severity_score > 0.2:
            severity = "MEDIUM"
        else:
            severity = "LOW"

        # Create incident
        incident = Incident.objects.create(
            log_file=log_file,
            title=f"Cluster {cluster_id} Incident",
            severity=severity,
            severity_score=severity_score,
            start_time=start_time,
            end_time=end_time,
            event_count=len(cluster_events),
        )

        # Generate summary
        summary = generate_incident_summary(incident, cluster_events)
        incident.summary = summary
        incident.save()

        # Link events
        for e in cluster_events:
            e.incident = incident

        incidents_created += 1

    return incidents_created

