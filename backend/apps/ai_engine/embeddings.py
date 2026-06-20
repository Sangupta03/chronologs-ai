import json
import logging
import os

import numpy as np
from django.conf import settings

logger = logging.getLogger(__name__)

EMBEDDING_MODEL = "models/gemini-embedding-001"
INDEX_DIR = settings.MEDIA_ROOT / "faiss_indexes"


def _configure():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return False

    import google.generativeai as genai

    genai.configure(api_key=api_key)
    return True


def embed_messages(messages):
    """
    Returns an (n, dim) float32 numpy array of embeddings for the given
    messages, or None if Gemini is unavailable/unconfigured/fails.
    """

    if not messages or not _configure():
        return None

    import google.generativeai as genai

    try:
        result = genai.embed_content(model=EMBEDDING_MODEL, content=messages)
        return np.array(result["embedding"], dtype="float32")
    except Exception:
        logger.exception("Gemini embedding generation failed")
        return None


def _index_paths(log_file_id):
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    return (
        INDEX_DIR / f"{log_file_id}.faiss",
        INDEX_DIR / f"{log_file_id}.json",
    )


def build_index(log_file_id, events):
    """
    Embeds each event's message and writes a FAISS index + a sidecar
    JSON mapping vector row -> LogEvent id, to disk. No-ops (returns
    False) if embeddings can't be generated.
    """

    import faiss

    events = list(events)
    messages = [e.message for e in events]

    vectors = embed_messages(messages)
    if vectors is None:
        return False

    dim = vectors.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(vectors)

    index_path, meta_path = _index_paths(log_file_id)
    faiss.write_index(index, str(index_path))
    meta_path.write_text(json.dumps([str(e.id) for e in events]))

    return True


def search_index(log_file_id, query, top_k=10):
    """
    Returns a list of (event_id, distance) tuples for the top_k closest
    matches to the query within the given log file's index. Returns None
    if no index exists or embeddings are unavailable.
    """

    import faiss

    index_path, meta_path = _index_paths(log_file_id)
    if not index_path.exists() or not meta_path.exists():
        return None

    query_vector = embed_messages([query])
    if query_vector is None:
        return None

    index = faiss.read_index(str(index_path))
    event_ids = json.loads(meta_path.read_text())

    k = min(top_k, index.ntotal)
    distances, indices = index.search(query_vector, k)

    return [
        (event_ids[idx], float(dist))
        for dist, idx in zip(distances[0], indices[0])
        if idx != -1
    ]
