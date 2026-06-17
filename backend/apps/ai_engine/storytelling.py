from collections import Counter


def extract_incident_facts(events):
    """
    Compute the structured facts about an incident's events.
    Used both to render the rule-based summary and as the
    grounding input for the LLM-generated narrative.
    """

    if not events:
        return None

    start_time = min(e.timestamp for e in events)
    end_time = max(e.timestamp for e in events)

    services = [e.service_name for e in events]
    service_counts = Counter(services)
    main_service = service_counts.most_common(1)[0][0]

    levels = [e.log_level for e in events]
    level_counts = Counter(levels)

    error_count = level_counts.get("ERROR", 0)
    anomaly_count = sum(1 for e in events if e.is_anomaly)
    total = len(events)

    error_ratio = (error_count / total) if total > 0 else 0

    messages = [e.message for e in events]
    message_counts = Counter(messages)
    sample_message = message_counts.most_common(1)[0][0]

    if error_ratio > 0.7:
        conclusion = "This likely indicates a critical system failure requiring immediate attention."
    elif error_ratio > 0.4:
        conclusion = "This suggests a significant issue impacting system stability."
    elif error_ratio > 0.1:
        conclusion = "This indicates a moderate level of instability that should be monitored."
    else:
        conclusion = "This appears to be minor or expected system behavior with low impact."

    return {
        "start_time": start_time,
        "end_time": end_time,
        "main_service": main_service,
        "total_events": total,
        "error_count": error_count,
        "anomaly_count": anomaly_count,
        "error_ratio": error_ratio,
        "sample_message": sample_message,
        "conclusion": conclusion,
    }


def render_rule_based_summary(facts):
    """
    Deterministic, template-based incident summary built from
    extract_incident_facts(). Used as the fallback when the LLM
    narrative generator is unavailable or fails.
    """

    if facts is None:
        return "No events available for this incident."

    return f"""
Between {facts['start_time'].strftime('%H:%M:%S')} and {facts['end_time'].strftime('%H:%M:%S')},
the {facts['main_service']} service experienced unusual activity.

A total of {facts['total_events']} log events were recorded, with {facts['error_count']} errors.

Most frequent issue observed: "{facts['sample_message']}".

Error rate was approximately {round(facts['error_ratio'] * 100, 2)}%.

{facts['conclusion']}
""".strip()


def generate_incident_summary(incident, events):
    """
    Generate human-readable explanation of an incident using the
    rule-based template only (no LLM). Kept for direct/standalone use.
    """
    return render_rule_based_summary(extract_incident_facts(events))