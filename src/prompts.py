"""
prompts.py
==========
Template prompt centralizzati.
"""

from __future__ import annotations

import json


def build_classifier_prompt(message: str) -> str:
    schema = {
        "label": "INFO|RIMBORSO|CHECKIN|COLAZIONE|ASSISTENZA|ALTRO",
        "urgency": "BASSA|MEDIA|ALTA",
        "summary": "string",
    }

    return f"""
Classifica il messaggio cliente.

MESSAGGIO:
{message}

Regole:
- Rispondi SOLO con JSON valido.
- NON usare markdown.
- Segui esattamente questo schema:

{json.dumps(schema, ensure_ascii=False, indent=2)}

Esempio risposta:
{{"label":"CHECKIN","urgency":"MEDIA","summary":"Chiede info su orario check-in."}}
""".strip()


def build_reply_prompt(
    user_message: str,
    label: str,
    urgency: str,
    summary: str,
    context: str,
) -> str:
    return f"""
Sei un assistente customer care per un hotel.

INFO INTERNA (classificazione):
- label: {label}
- urgenza: {urgency}
- riassunto: {summary}

REGOLA IMPORTANTISSIMA:
- Rispondi SOLO usando il CONTESTO qui sotto.
- Se il contesto non contiene la risposta, scrivi ESATTAMENTE:
  Non ho informazioni sufficienti.

CONTESTO:
{context}

MESSAGGIO CLIENTE:
{user_message}

Output:
- Risposta breve e chiara (max 8 righe)
- Tono professionale e cortese
""".strip()