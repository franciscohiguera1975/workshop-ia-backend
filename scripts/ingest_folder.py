"""Carga todos los .txt/.pdf de backend/documents/ a la base RAG,
troceados en fragmentos de ~400 palabras. Correr desde backend/:

    python scripts/ingest_folder.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import rag  # noqa: E402

DOCS_DIR = Path(__file__).resolve().parent.parent / "documents"
MAX_WORDS = 400


def read_text(path: Path) -> str:
    if path.suffix.lower() == ".pdf":
        from pypdf import PdfReader

        reader = PdfReader(str(path))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    return path.read_text(encoding="utf-8")


def chunk_text(text: str, max_words: int = MAX_WORDS) -> list[str]:
    words = text.split()
    return [" ".join(words[i : i + max_words]) for i in range(0, len(words), max_words)]


def main():
    if not DOCS_DIR.exists():
        print(f"No existe {DOCS_DIR} — créala y coloca ahí tu .txt o .pdf.")
        return

    archivos = [p for p in DOCS_DIR.iterdir() if p.suffix.lower() in (".txt", ".pdf")]
    if not archivos:
        print(f"{DOCS_DIR} está vacía — no hay .txt ni .pdf que cargar.")
        return

    for path in archivos:
        texto = read_text(path)
        fragmentos = chunk_text(texto)
        print(f"{path.name}: {len(texto.split())} palabras -> {len(fragmentos)} fragmentos")

        for i, fragmento in enumerate(fragmentos, start=1):
            rag.add_document(title=f"{path.stem} — parte {i}", text=fragmento)

    print("\nListo. Para ver los vectores resultantes: python scripts/inspect_embeddings.py")


if __name__ == "__main__":
    main()
