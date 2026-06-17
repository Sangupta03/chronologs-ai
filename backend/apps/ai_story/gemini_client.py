import logging
import os

logger = logging.getLogger(__name__)

_model = None
_configured = False


def _get_model():
    global _model, _configured

    if _configured:
        return _model

    _configured = True

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return None

    import google.generativeai as genai

    genai.configure(api_key=api_key)
    _model = genai.GenerativeModel("gemini-2.5-flash")
    return _model


def _build_prompt(incident, facts):
    return f"""You are an SRE assistant explaining a detected incident to an on-call engineer.

Incident severity: {incident.severity} (score {round(incident.severity_score, 2)})
Service: {facts['main_service']}
Time window: {facts['start_time']} to {facts['end_time']}
Total events: {facts['total_events']}
Error count: {facts['error_count']}
Anomaly count: {facts['anomaly_count']}
Error rate: {round(facts['error_ratio'] * 100, 1)}%
Most frequent log message: "{facts['sample_message']}"

Write a concise (3-5 sentence) incident summary for the engineer covering:
1. What likely happened and which service is affected.
2. How severe this is and why.
3. One concrete suggested next step to investigate or mitigate.

Do not use markdown headers. Plain prose only."""


def generate_narrative(incident, facts):
    """
    Returns an LLM-written incident narrative, or None if Gemini is
    unavailable/unconfigured/fails. Caller is responsible for falling
    back to the rule-based summary in that case.
    """

    if facts is None:
        return None

    model = _get_model()
    if model is None:
        return None

    try:
        response = model.generate_content(_build_prompt(incident, facts))
        text = (response.text or "").strip()
        return text or None
    except Exception:
        logger.exception("Gemini narrative generation failed; falling back to rule-based summary")
        return None
