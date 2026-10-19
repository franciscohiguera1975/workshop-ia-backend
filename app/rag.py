import lancedb
from lancedb.pydantic import LanceModel, Vector

from .embeddings import get_embedding_function

_embedding_fn = get_embedding_function()


class Document(LanceModel):
    title: str
    text: str = _embedding_fn.SourceField()
    vector: Vector(_embedding_fn.ndims()) = _embedding_fn.VectorField()


_db = lancedb.connect("./storage/lancedb")
_table = _db.create_table("documents", schema=Document, exist_ok=True)


def add_document(title: str, text: str) -> None:
    _table.add([{"title": title, "text": text}])


def list_documents() -> list[dict]:
    return [{"title": r["title"], "text": r["text"]} for r in _table.to_arrow().to_pylist()]


def search(query: str, top_k: int = 2) -> list[dict]:
    if _table.count_rows() == 0:
        return []
    results = _table.search(query).limit(top_k).to_list()
    return [
        {"title": r["title"], "text": r["text"], "score": round(1 / (1 + r["_distance"]), 3)}
        for r in results
    ]
