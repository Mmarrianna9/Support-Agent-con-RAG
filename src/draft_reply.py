"""
draft_reply.py
==============
Generazione bozza risposta con guardrail:
- usa SOLO il contesto
- se non basta -> "Non ho informazioni sufficienti."
"""

from __future__ import annotations

from api_client import chat
from prompts import build_reply_prompt


def draft_reply(
    user_message: str,
    label: str,
    urgency: str,
    summary: str,
    context: str,
) -> str:
    prompt = build_reply_prompt(
        user_message=user_message,
        label=label,
        urgency=urgency,
        summary=summary,
        context=context,
    )
    return chat(
        model="gpt-4o-mini",
        temperature=0.4,
        messages=[{"role": "user", "content": prompt}],
    )