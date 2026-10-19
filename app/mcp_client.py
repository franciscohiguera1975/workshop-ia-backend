import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from .llm_client import get_llm_client

SERVER_PARAMS = StdioServerParameters(command=sys.executable, args=["mcp_server.py"])


def _mcp_tool_to_schema(tool) -> dict:
    return {
        "type": "function",
        "function": {
            "name": tool.name,
            "description": tool.description or "",
            "parameters": tool.input_schema,
        },
    }


async def run_agent_with_mcp(messages: list[dict], max_steps: int = 4) -> tuple[str, list[dict]]:
    client = get_llm_client()
    trace: list[dict] = []

    async with stdio_client(SERVER_PARAMS) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools_response = await session.list_tools()
            tools_schema = [_mcp_tool_to_schema(t) for t in tools_response.tools]

            for _ in range(max_steps):
                result = client.chat_with_tools(messages, tools_schema)

                if not result.tool_calls:
                    return result.content or "", trace

                messages.append({
                    "role": "assistant",
                    "content": result.content or "",
                    "tool_calls": result.raw_tool_calls,
                })

                for call in result.tool_calls:
                    tool_result = await session.call_tool(call["name"], call["arguments"])
                    output = "\n".join(
                        part.text for part in tool_result.content if hasattr(part, "text")
                    )
                    trace.append({"name": call["name"], "args": call["arguments"], "result": output})
                    messages.append({
                        "role": "tool",
                        "tool_call_id": call["id"],
                        "content": output,
                    })

    return "No pude completar la tarea tras varios pasos de herramientas.", trace
