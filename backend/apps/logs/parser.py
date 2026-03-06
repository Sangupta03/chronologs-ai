import re
from datetime import datetime
from .models import LogEvent

import hashlib
PATTERNS = [
    re.compile(r"(?P<timestamp>\S+ \S+) (?P<level>\w+) (?P<service>\S+) (?P<message>.+)"),
]


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


def parse_log_file(log_file):

    events_buffer = []

    events_parsed = 0
    events_failed = 0

    with open(log_file.file.path, "r") as f:

        for line in f:

            parsed = parse_log_line(line.strip())

            if not parsed:
                events_failed += 1
                continue

            try:
                timestamp = datetime.strptime(parsed["timestamp"], "%Y-%m-%d %H:%M:%S")
            except:
                events_failed += 1
                continue

            event = LogEvent(
                log_file=log_file,
                timestamp=timestamp,
                log_level=parsed["level"],
                service_name=parsed["service"],
                message=parsed["message"],
                raw_log=line.strip(),
                event_hash = hashlib.sha256(line.strip().encode()).hexdigest(),
            )

            events_buffer.append(event)
            events_parsed += 1

            if len(events_buffer) >= 500:
                LogEvent.objects.bulk_create(events_buffer)
                events_buffer.clear()

    if events_buffer:
        LogEvent.objects.bulk_create(events_buffer)

    return events_parsed, events_failed