from apps.logs.models import LogEvent
from .vectorizer import vectorize_logs
from .clustering import cluster_logs
from .anomaly import detect_anomalies
from .incident_engine import create_incidents


def compute_k(n_messages):
    """Number of clusters to use, scaling with dataset size, capped at 8."""
    return max(1, min(8, n_messages // 15))


def run_analysis(log_file):
    """
    Runs the full clustering/anomaly/incident pipeline for a LogFile.
    Callable from a view, a Celery task, or a test - no HTTP plumbing.
    Raises ValueError if there are no events to analyze.
    """

    events = LogEvent.objects.filter(log_file=log_file)

    if not events.exists():
        raise ValueError("No events found")

    messages = [event.message for event in events]

    vectors, _ = vectorize_logs(messages)

    k = compute_k(len(messages))
    labels, _ = cluster_logs(vectors, k=k)

    anomalies, _ = detect_anomalies(vectors)

    for event, label, anomaly in zip(events, labels, anomalies):
        event.cluster_id = int(label)
        event.is_anomaly = bool(anomaly)

    LogEvent.objects.bulk_update(events, ["cluster_id", "is_anomaly"])

    events = LogEvent.objects.filter(log_file=log_file)

    incident_count = create_incidents(log_file, events)

    cluster_counts = {}
    for label in labels:
        label = int(label)
        cluster_counts[label] = cluster_counts.get(label, 0) + 1

    return {
        "status": "analysis completed",
        "total_events": len(messages),
        "clusters": cluster_counts,
        "incidents_created": incident_count,
    }
