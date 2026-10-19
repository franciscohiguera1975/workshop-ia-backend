from openai import OpenAI

from .config import get_settings


class OpenAICompatibleClient:
    """Sirve para vLLM local, Groq y la API de OpenAI (ChatGPT): los tres
    exponen la misma API — solo cambian base_url/api_key/model. Por eso un
    único cliente alcanza para los tres (y para cualquier otro proveedor
    que hable el mismo protocolo, ver tutorial/00 §0.2)."""

    def __init__(self, base_url: str, api_key: str, model: str):
        self._client = OpenAI(base_url=base_url, api_key=api_key)
        self._model = model

    def chat(self, messages: list[dict]) -> str:
        response = self._client.chat.completions.create(
            model=self._model, messages=messages
        )
        return response.choices[0].message.content or ""


def get_llm_client() -> OpenAICompatibleClient:
    settings = get_settings()

    if not settings.llm_api_key:
        raise RuntimeError(
            "Falta LLM_API_KEY en backend/.env — ver tutorial/00 §0.2 para "
            "obtener una clave de Groq, OpenAI o tu proveedor elegido."
        )

    return OpenAICompatibleClient(
        settings.llm_base_url, settings.llm_api_key, settings.llm_model
    )
