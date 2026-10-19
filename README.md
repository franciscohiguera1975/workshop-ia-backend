# Backend — Workshop IA

Repositorio propio (independiente de `tutoriales/`, con su propio
historial de git) organizado **por ramas, una por módulo del taller**. Cada
rama contiene el backend exactamente como queda al terminar ese módulo del
tutorial — así puedes saltar de rama en rama y probar hasta dónde va el
código en cada punto, sin tener que reconstruir nada a mano.

## Ramas

| Rama | Corresponde a | Qué agrega |
|---|---|---|
| `00-setup` | [`tutorial/00-bienvenida-y-setup.md`](../tutorial/00-bienvenida-y-setup.md) | Carpeta vacía — punto de partida |
| `01-chat-simple` | [`tutorial/01-chat-simple.md`](../tutorial/01-chat-simple.md) | `GET /health`, `POST /chat` contra un LLM real |
| `02-skills` | [`tutorial/02-skills.md`](../tutorial/02-skills.md) | Selección de instrucciones especializadas (`app/skills.py`) |
| `03-rag` | [`tutorial/03-rag.md`](../tutorial/03-rag.md) | Documentos propios vía LanceDB + embeddings (`app/rag.py`, `app/embeddings.py`, `/documents`) |
| `04-agentes` | [`tutorial/04-agentes.md`](../tutorial/04-agentes.md) | Loop de *tool calling* (`app/tools.py`, `app/agent.py`) |
| `05-mcp` | [`tutorial/05-mcp.md`](../tutorial/05-mcp.md) | Herramientas servidas por un servidor MCP propio (`mcp_server.py`, `app/mcp_client.py`) |
| `main` | — | Consolidado: igual que `05-mcp`, con todos los módulos integrados |

El historial es **lineal** — cada rama nace de la anterior (`01-chat-simple`
← `00-setup` ← …), así que el `diff` entre dos ramas consecutivas es
exactamente el código nuevo de ese módulo:

```bash
git diff 02-skills..03-rag    # qué agrega el Módulo 03 sobre el 02
```

## Probar una rama

```bash
git checkout 03-rag           # o la rama que quieras probar
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # completar con tu API key (ver tutorial/00 §0.2)
uvicorn app.main:app --reload --port 8000
```

`storage/`, `.venv/` y `.env` están en `.gitignore` — no interfieren al
cambiar de rama.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

## Ejecutar

```bash
uvicorn app.main:app --reload --port 8000
```

- Docs interactivas: http://localhost:8000/docs
- Salud: http://localhost:8000/health

## Probar sin frontend

```bash
curl -s http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hola, ¿qué puedes hacer?", "history": []}' | python3 -m json.tool
```

Necesitas una API key real en `.env` (ver `tutorial/00-bienvenida-y-setup.md`
§0.2) — este proyecto no incluye un modo mock.
