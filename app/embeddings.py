from typing import List, Union

from lancedb.embeddings import TextEmbeddingFunction, register
from lancedb.embeddings.registry import get_registry


@register("openai_compatible_embeddings")
class OpenAICompatibleEmbeddings(TextEmbeddingFunction):
    """Embeddings reales vía cualquier endpoint compatible con OpenAI
    (la API de OpenAI, Gemini o vLLM sirviendo un modelo de embeddings)."""

    name: str
    base_url: str
    api_key: str
    dim: int = 1536
    send_dimensions: bool = False

    def ndims(self) -> int:
        return self.dim

    def generate_embeddings(self, texts: Union[List[str], "np.ndarray"]) -> List[list]:
        from openai import OpenAI

        client = OpenAI(base_url=self.base_url, api_key=self.api_key)
        extra = {"dimensions": self.dim} if self.send_dimensions else {}
        response = client.embeddings.create(model=self.name, input=list(texts), **extra)
        return [d.embedding for d in response.data]


def get_embedding_function():
    from .config import get_settings

    settings = get_settings()
    registry = get_registry()

    if settings.embedding_provider == "local":
        # sentence-transformers: corre en esta máquina, sin API key ni
        # costo. Es la función nativa de LanceDB, no la de arriba.
        return registry.get("sentence-transformers").create(
            name=settings.embedding_model,
            device="cpu",
        )

    return registry.get("openai_compatible_embeddings").create(
        name=settings.embedding_model,
        base_url=settings.embedding_base_url,
        api_key=settings.embedding_api_key,
        dim=settings.embedding_dim,
        send_dimensions=settings.embedding_provider == "gemini",
    )
