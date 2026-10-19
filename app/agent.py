from .llm_client import get_llm_client
from .tools import TOOLS_SCHEMA, TOOLS_IMPL


def run_agent(messages: list[dict], max_steps: int = 4) -> tuple[str, list[dict]]:
    client = get_llm_client()
    trace: list[dict] = []

    for _ in range(max_steps):
        result = client.chat_with_tools(messages, TOOLS_SCHEMA)

        if not result.tool_calls:
            return result.content or "", trace

        messages.append({
            "role": "assistant",
            "content": result.content or "",
            "tool_calls": result.raw_tool_calls,
        })

        for call in result.tool_calls:
            fn = TOOLS_IMPL.get(call["name"])
            output = fn(**call["arguments"]) if fn else f"Herramienta desconocida: {call['name']}"
            trace.append({"name": call["name"], "args": call["arguments"], "result": output})
            messages.append({
                "role": "tool",
                "tool_call_id": call["id"],
                "content": output,
            })

    return "No pude completar la tarea tras varios pasos de herramientas.", trace
