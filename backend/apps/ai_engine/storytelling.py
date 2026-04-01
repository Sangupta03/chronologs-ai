from collections import Counter


def generate_incident_summary(incident, events):
    """
    Generate human-readable explanation of an incident
    """

    if not events:
        return "No events available for this incident."

    # 1️⃣ Time window
    start_time = min(e.timestamp for e in events)
    end_time = max(e.timestamp for e in events)

    # 2️⃣ Service distribution
    services = [e.service_name for e in events]
    service_counts = Counter(services)
    main_service = service_counts.most_common(1)[0][0]

    # 3️⃣ Log levels
    levels = [e.log_level for e in events]
    level_counts = Counter(levels)

    error_count = level_counts.get("ERROR", 0)
    total = len(events)

    error_ratio = (error_count / total) if total > 0 else 0

    # 4️⃣ Most frequent message (better than first message)
    messages = [e.message for e in events]
    message_counts = Counter(messages)
    sample_message = message_counts.most_common(1)[0][0]

    # 5️⃣ Smart conclusion
    if error_ratio > 0.7:
        conclusion = "This likely indicates a critical system failure requiring immediate attention."
    elif error_ratio > 0.4:
        conclusion = "This suggests a significant issue impacting system stability."
    elif error_ratio > 0.1:
        conclusion = "This indicates a moderate level of instability that should be monitored."
    else:
        conclusion = "This appears to be minor or expected system behavior with low impact."

    # 6️⃣ Generate summary
    summary = f"""
Between {start_time.strftime('%H:%M:%S')} and {end_time.strftime('%H:%M:%S')},
the {main_service} service experienced unusual activity.

A total of {total} log events were recorded, with {error_count} errors.

Most frequent issue observed: "{sample_message}".

Error rate was approximately {round(error_ratio * 100, 2)}%.

{conclusion}
""".strip()

    return summary