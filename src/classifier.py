"""
classifier.py
=============
Classificazione intent + urgenza.

Online:
- usa OpenAI e richiede JSON.

Fallback offline:
- regole keyword (per non bloccare demo).

Output:
{"label": "...", "urgency": "...", "summary": "..."}
"""

from __future__ import annotations

import json
from typing import Dict

from api_client import chat
from prompts import build_classifier_prompt


def _rule_based(message: str) -> Dict[str, str]:
    m = message.lower()

    if any(w in m for w in ["urgente", "subito", "immediato", "oggi", "asap"]):
        urgency = "ALTA"
    elif any(w in m for w in ["domani", "presto", "rapidamente"]):
        urgency = "MEDIA"
    else:
        urgency = "BASSA"

    if any(w in m for w in ["rimborso", "cancell", "annull"]):
        label = "RIMBORSO"
    elif "check-in" in m or "check in" in m or "arrivo" in m:
        label = "CHECKIN"
    elif "colazione" in m or "breakfast" in m:
        label = "COLAZIONE"
    elif any(w in m for w in ["aiuto", "problema", "assistenza", "supporto"]):
        label = "ASSISTENZA"
    else:
        label = "INFO"

    summary = message.strip().split("\n")[0][:120]
    return {"label": label, "urgency": urgency, "summary": summary}


def classify_message(message: str) -> Dict[str, str]:
    try:
        prompt = build_classifier_prompt(message)
        out = chat(
            model="gpt-4o-mini",
            temperature=0,
            messages=[{"role": "user", "content": prompt}],
        )
        data = json.loads(out)

        label = str(data.get("label", "")).strip().upper()
        urgency = str(data.get("urgency", "")).strip().upper()
        summary = str(data.get("summary", "")).strip()

        allowed_labels = {"INFO", "RIMBORSO", "CHECKIN", "COLAZIONE", "ASSISTENZA", "ALTRO"}
        allowed_urg = {"BASSA", "MEDIA", "ALTA"}

        if label not in allowed_labels or urgency not in allowed_urg or not summary:
            return _rule_based(message)

        return {"label": label, "urgency": urgency, "summary": summary}
    except Exception:
        return _rule_based(message)