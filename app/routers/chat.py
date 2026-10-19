from fastapi import APIRouter
from pydantic import BaseModel

from .. import rag
from ..mcp_client import run_agent_with_mcp
from ..skills import select_skill

router = APIRouter()


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    history: list[Message] = []


class SkillUsed(BaseModel):
    name: str
    reason: str | None = None


class Source(BaseModel):
    title: str
    snippet: str
    score: float | None = None


class ToolCall(BaseModel):
    name: str
    args: dict | None = None
    result: str | None = None


class ChatResponse(BaseModel):
    reply: str
    skill_used: SkillUsed | None = None
    sources: list[Source] | None = None
    tool_calls: list[ToolCall] | None = None


class DocumentIn(BaseModel):
    title: str
    text: str


@router.post("/documents")
def add_document(doc: DocumentIn):
    rag.add_document(doc.title, doc.text)
    return {"status": "ok"}


@router.get("/documents")
def get_documents():
    return rag.list_documents()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    messages = [{"role": m.role, "content": m.content} for m in request.history]

    skill = select_skill(request.message)
    skill_used = None
    if skill:
        messages.insert(0, {"role": "system", "content": skill["instructions"]})
        skill_used = SkillUsed(name=skill["name"], reason=f'Palabras clave de "{skill["name"]}" detectadas.')

    messages.append({"role": "user", "content": request.message})
    reply, trace = await run_agent_with_mcp(messages)

    tool_calls = [ToolCall(**t) for t in trace] if trace else None
    return ChatResponse(reply=reply, skill_used=skill_used, tool_calls=tool_calls)
