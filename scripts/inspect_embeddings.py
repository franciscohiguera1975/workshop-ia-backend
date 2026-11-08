"""Muestra por consola cómo quedaron los documentos cargados después de
convertirse a embeddings: dimensión real del vector y sus primeros
valores. Correr desde backend/:

    python scripts/inspect_embeddings.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import rag  # noqa: E402


def main():
    docs = rag.inspect_vectors(limit=10)
    if not docs:
        print("No hay documentos cargados todavía (usa /documents o scripts/ingest_folder.py).")
        return

    for d in docs:
        preview = ", ".join(f"{v:.4f}" for v in d["vector_preview"])
        print(f"- {d['title']!r}")
        print(f"    dimensiones: {d['vector_dim']}")
        print(f"    primeros valores: [{preview}, ...]")


if __name__ == "__main__":
    main()
