from fastapi import APIRouter
from pydantic import BaseModel

from .. import rag
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


class Source(BaseModel):
    title: str
    snippet: str
    score: float | None = None


class ChatResponse(BaseModel):
    reply: str
    skill_used: SkillUsed | None = None
    sources: list[Source] | None = None


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

    retrieved = rag.search(request.message)
    sources = None
    if retrieved:
        context = "\n\n".join(f'[{d["title"]}] {d["text"]}' for d in retrieved)
        messages.insert(0, {
            "role": "system",
            "content": f"Usa el siguiente contexto si es relevante. Si no, ignóralo.\n\n{context}",
        })
        sources = [Source(title=d["title"], snippet=d["text"], score=d["score"]) for d in retrieved]

    messages.append({"role": "user", "content": request.message})
    reply = client.chat(messages)

    return ChatResponse(reply=reply, skill_used=skill_used, sources=sources)
