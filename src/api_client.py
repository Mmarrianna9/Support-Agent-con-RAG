"""
api_client.py
=============
Wrapper semplice per OpenAI.

- Legge OPENAI_API_KEY da key.env o variabili ambiente.
- Fornisce:
  - chat(messages, model=..., temperature=...)
  - embed(texts, model=...)

Se manca la chiave, alza un errore chiaro.
"""

from __future__ import annotations

import os
from typing import Iterable, List, Dict

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv("key.env")


def _get_client() -> OpenAI:
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError(
            "OPENAI_API_KEY mancante. Inseriscila in key.env oppure nelle variabili ambiente."
        )
    return OpenAI(api_key=key)


def chat(
    messages: List[Dict[str, str]],
    model: str = "gpt-4o-mini",
    temperature: float = 0.2,
) -> str:
    client = _get_client()
    resp = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return resp.choices[0].message.content.strip()


def embed(
    texts: Iterable[str],
    model: str = "text-embedding-3-small",
) -> List[List[float]]:
    client = _get_client()
    resp = client.embeddings.create(model=model, input=list(texts))
    return [item.embedding for item in resp.data]
