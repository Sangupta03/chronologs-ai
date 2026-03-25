import re
import hashlib
from datetime import datetime

from .models import LogEvent


# -----------------------------
# Log format patterns
# -----------------------------
PATTERNS = [

    # Format 1
    # 2026-03-07 12:01:33 ERROR payment-service Database connection timeout
    re.compile(
        r"(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) "
        r"(?P<level>\w+) "
        r"(?P<service>\S+) "
        r"(?P<message>.+)"
    ),

    # Format 2
    # [ERROR] 2026-03-07T12:01:33 payment-service: DB connection failed
    re.compile(
        r"\[(?P<level>\w+)\] "
        r"(?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}) "
        r"(?P<service>\S+): "
        r"(?P<message>.+)"
    ),

    # Format 3
    # INFO 2026-03-07 user-service request completed
    re.compile(
        r"(?P<level>\w+) "
        r"(?P<timestamp>\d{4}-\d{2}-\d{2}) "
        r"(?P<service>\S+) "
        r"(?P<message>.+)"
    ),
]


# -----------------------------
# Timestamp parsing helper
# -----------------------------
def parse_timestamp(ts):

    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d",
    ]

    for fmt in formats:
        try:
            return datetime.strptime(ts, fmt)
        except:
            continue

    return None
# FOR NORMALIZATION

def normalize_level(level):

    level = level.upper()

    mapping = {
        "WARNING": "WARN",
        "WARN": "WARN",
        "ERROR": "ERROR",
        "ERR": "ERROR",
        "INFO": "INFO",
        "DEBUG": "DEBUG",
        "CRITICAL": "CRITICAL",
    }

    return mapping.get(level, "INFO")

# -----------------------------
# Parse single log line
# -----------------------------
def parse_log_line(line):

    for pattern in PATTERNS:

        match = pattern.match(line)

        if match:
            data = match.groupdict()

            return {
                "timestamp": data["timestamp"],
                "level": data["level"],
                "service": data["service"],
                "message": data["message"],
            }

    return None


# -----------------------------
# Parse entire log file
# -----------------------------
def parse_log_file(log_file):

    events_buffer = []

    events_parsed = 0
    events_failed = 0

    with open(log_file.file.path, "r") as f:

        for line in f:

            line = line.strip()

            parsed = parse_log_line(line)

            if not parsed:
                events_failed += 1
                continue

            timestamp = parse_timestamp(parsed["timestamp"])

            if not timestamp:
                events_failed += 1
                continue

            event = LogEvent(
                log_file=log_file,
                timestamp=timestamp,
                log_level=normalize_level(parsed["level"]),
                service_name=parsed["service"],
                message=parsed["message"],
                raw_log=line,
                event_hash=hashlib.sha256(line.encode()).hexdigest(),
            )

            events_buffer.append(event)
            events_parsed += 1

            # Batch insert every 500 events
            if len(events_buffer) >= 500:
                LogEvent.objects.bulk_create(events_buffer)
                events_buffer.clear()

    # Insert remaining events
    if events_buffer:
        LogEvent.objects.bulk_create(events_buffer)

    return events_parsed, events_failed