from fastapi import APIRouter
from pydantic import BaseModel

from ..llm_client import get_llm_client
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


class ChatResponse(BaseModel):
    reply: str
    skill_used: SkillUsed | None = None


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    client = get_llm_client()

    messages = [{"role": m.role, "content": m.content} for m in request.history]

    skill = select_skill(request.message)
    skill_used = None
    if skill:
        messages.insert(0, {"role": "system", "content": skill["instructions"]})
        skill_used = SkillUsed(
            name=skill["name"],
            reason=f'Se detectaron las palabras clave de "{skill["name"]}" en tu mensaje.',
        )

    messages.append({"role": "user", "content": request.message})
    reply = client.chat(messages)

    return ChatResponse(reply=reply, skill_used=skill_used)
