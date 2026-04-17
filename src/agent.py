"""
agent.py
========
Orchestratore: classifica -> retrieval -> draft -> report
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

from classifier import classify_message
from retrieval import retrieve_context
from draft_reply import draft_reply
from reporting import save_run_report


@dataclass
class AgentResult:
    label: str
    urgency: str
    summary: str
    context: str
    reply: str
    meta: Dict[str, Any]


class SupportAgent:
    def __init__(self, top_k: int = 3) -> None:
        self.top_k = top_k

    def run(self, user_message: str) -> AgentResult:
        cls = classify_message(user_message)
        ctx = retrieve_context(user_message, top_k=self.top_k)

        reply_text = draft_reply(
            user_message=user_message,
            label=cls["label"],
            urgency=cls["urgency"],
            summary=cls["summary"],
            context=ctx["context"],
        )

        meta = {
            "classifier": cls,
            "retrieval": {k: v for k, v in ctx.items() if k != "context"},
        }

        paths = save_run_report(
            user_message=user_message,
            label=cls["label"],
            urgency=cls["urgency"],
            summary=cls["summary"],
            context=ctx["context"],
            reply=reply_text,
            meta=meta,
        )

        return AgentResult(
            label=cls["label"],
            urgency=cls["urgency"],
            summary=cls["summary"],
            context=ctx["context"],
            reply=reply_text,
            meta={"files": paths, **meta},
        )