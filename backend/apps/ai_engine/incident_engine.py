from collections import defaultdict

from apps.incidents.models import Incident


def create_incidents(log_file, events):

    cluster_groups = defaultdict(list)

    # Group events by cluster
    for event in events:
        cluster_groups[event.cluster_id].append(event)

    incidents_created = 0

    for cluster_id, cluster_events in cluster_groups.items():

        error_count = sum(1 for e in cluster_events if e.log_level == "ERROR")
        anomaly_count = sum(1 for e in cluster_events if e.is_anomaly)

        # Simple rule for incident
        if error_count > 0 or anomaly_count > 0:

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

            incident = Incident.objects.create(
                log_file=log_file,
                title=f"Cluster {cluster_id} Incident",
                severity=severity,
                severity_score=severity_score,
                start_time=start_time,
                end_time=end_time,
                event_count=len(cluster_events),
            )

            # Link events to incident
            for e in cluster_events:
                e.incident = incident

            incidents_created += 1

    return incidents_created

