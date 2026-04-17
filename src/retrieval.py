import json
import os
from typing import Dict, List, Any

try:
    import numpy as np
except Exception:
    np = None

from api_client import embed

KB_PATH = os.path.join("kb", "knowledge.json")


def load_kb() -> List[Dict[str, str]]:
    if not os.path.exists(KB_PATH):
        raise FileNotFoundError("kb/knowledge.json non trovato.")
    with open(KB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _dot(a: List[float], b: List[float]) -> float:
    if np is not None:
        return float(np.dot(np.array(a), np.array(b)))
    return float(sum(x * y for x, y in zip(a, b)))


def retrieve_context(query: str, top_k: int = 3) -> Dict[str, Any]:
    kb_docs = load_kb()
    docs = [d["text"] for d in kb_docs]

    doc_vecs = embed(docs)
    q_vec = embed([query])[0]

    scores = [_dot(q_vec, v) for v in doc_vecs]
    ranked = sorted(list(enumerate(scores)), key=lambda x: x[1], reverse=True)[:top_k]

    context_parts = []
    top_ids = []
    top_scores = []

    for i, score in ranked:
        top_ids.append(kb_docs[i]["id"])
        top_scores.append(score)
        context_parts.append(f"[{kb_docs[i]['id']}] {kb_docs[i]['text']}")

    return {
        "context": "\n\n".join(context_parts),
        "top_k": top_ids,
        "scores": top_scores,
    }