import time

from celery import shared_task

from .models import LogFile
from .parser import parse_log_file


@shared_task
def process_log_file(log_file_id):
    log_file = LogFile.objects.get(id=log_file_id)

    start_time = time.time()

    try:
        events_parsed, events_failed = parse_log_file(log_file)
    except ValueError as exc:
        log_file.status = "failed"
        log_file.save()
        return {"status": "failed", "error": str(exc)}

    log_file.status = "parsed"
    log_file.total_events = events_parsed
    log_file.events_parsed = events_parsed
    log_file.events_failed = events_failed
    log_file.processing_time = round(time.time() - start_time, 2)
    log_file.save()

    return {
        "status": "parsed",
        "events_parsed": events_parsed,
        "events_failed": events_failed,
    }
