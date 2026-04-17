"""
main.py
=======
CLI: fai più domande (multi-turn).
- Scrivi il messaggio cliente (può essere multi-linea).
- Riga vuota -> invia il messaggio all'agente.
- Scrivi END (da solo su una riga) -> termina il programma.
"""

from __future__ import annotations

import os
from agent import SupportAgent

# Creiamo solo le cartelle che usiamo davvero
for folder in ["kb", "logs", "runs"]:
    os.makedirs(folder, exist_ok=True)


def read_multiline() -> str | None:
    """
    Legge un messaggio multi-linea.

    Regole:
    - Riga vuota: fine messaggio (invia all'agente)
    - END (da solo su una riga): termina il programma (ritorna None)
    """
    print("\nIncolla il messaggio cliente.")
    print("- Riga vuota = invia")
    print("- END = esci\n")

    lines: list[str] = []

    while True:
        line = input()

        # Se END è scritto da solo su una riga, usciamo
        if line.strip().upper() == "END":
            return None

        # Riga vuota: fine del messaggio
        if line.strip() == "":
            break

        lines.append(line)

    return "\n".join(lines).strip()


def main() -> None:
    agent = SupportAgent(top_k=3)

    while True:
        msg = read_multiline()

        # END -> stop programma
        if msg is None:
            print("👋 Chiusura programma (END).")
            break

        # Messaggio vuoto (es. invio subito) -> riparti
        if not msg:
            print("⚠️ Messaggio vuoto. Riprova.")
            continue

        # Esegui agente
        result = agent.run(msg)

        print("\n================ RISPOSTA (BOZZA) ================\n")
        print(result.reply)

        files = result.meta.get("files", {})
        if files:
            print("\n================ FILE GENERATI ================\n")
            for k, v in files.items():
                print(f"- {k}: {v}")

        print("\n================ METADATI ================\n")
        print(f"Label: {result.label} | Urgenza: {result.urgency}")
        print(f"Summary: {result.summary}")


if __name__ == "__main__":
    main()