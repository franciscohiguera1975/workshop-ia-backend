import json
from dataclasses import dataclass, field

from openai import OpenAI

from .config import get_settings


@dataclass
class ToolCallResult:
    content: str | None
    tool_calls: list[dict] = field(default_factory=list)
    raw_tool_calls: list | None = None


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

    def chat_with_tools(self, messages: list[dict], tools: list[dict]) -> ToolCallResult:
        response = self._client.chat.completions.create(
            model=self._model, messages=messages, tools=tools
        )
        message = response.choices[0].message

        if not message.tool_calls:
            return ToolCallResult(content=message.content or "")

        calls = [
            {
                "id": tc.id,
                "name": tc.function.name,
                "arguments": json.loads(tc.function.arguments or "{}"),
            }
            for tc in message.tool_calls
        ]
        raw = [
            {
                "id": tc.id,
                "type": "function",
                "function": {"name": tc.function.name, "arguments": tc.function.arguments},
            }
            for tc in message.tool_calls
        ]
        return ToolCallResult(content=message.content, tool_calls=calls, raw_tool_calls=raw)


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
