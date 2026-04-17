"""
reporting.py
============
Salva:
- report JSON (classificazione + retrieval + risposta)
- reply TXT

Ritorna i path dei file creati.
"""

from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Any, Dict


LOG_DIR = "logs"

def write_log(text: str):
    os.makedirs(LOG_DIR, exist_ok=True)
    with open(os.path.join(LOG_DIR, "agent.log"), "a", encoding="utf-8") as f:
        f.write(text + "\n")


def _safe_mkdir(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)


def save_run_report(
    user_message: str,
    label: str,
    urgency: str,
    summary: str,
    context: str,
    reply: str,
    meta: Dict[str, Any] | None = None,
    out_dir: str = "runs",
) -> Dict[str, str]:
    _safe_mkdir(out_dir)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    report_path = os.path.join(out_dir, f"run_{ts}.json")
    reply_path = os.path.join(out_dir, f"reply_{ts}.txt")

    payload = {
        "timestamp": ts,
        "user_message": user_message,
        "classification": {"label": label, "urgency": urgency, "summary": summary},
        "context": context,
        "reply": reply,
        "meta": meta or {},
    }

    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    with open(reply_path, "w", encoding="utf-8") as f:
        f.write(reply)

    write_log(f"Run salvata: {report_path}")

    return {"report_json": report_path, "reply_txt": reply_path}