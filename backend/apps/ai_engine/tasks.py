from celery import shared_task

from apps.logs.models import LogEvent, LogFile
from .embeddings import build_index
from .pipeline import run_analysis


@shared_task
def analyze_log_file(log_file_id):
    log_file = LogFile.objects.get(id=log_file_id)
    log_file.status = "clustered"
    log_file.save()

    try:
        result = run_analysis(log_file)
    except ValueError as exc:
        log_file.status = "failed"
        log_file.analysis_error = str(exc)
        log_file.save()
        return {"status": "failed", "error": str(exc)}

    log_file.status = "completed"
    log_file.analysis_result = result
    log_file.analysis_error = None
    log_file.save()

    events = LogEvent.objects.filter(log_file=log_file)
    build_index(log_file_id, events)

    return result
