from mcp.server.mcpserver import MCPServer

from app.tools import calculate, get_clima
from app.rag import search as rag_search

mcp = MCPServer("workshop-tools")


@mcp.tool()
def calcular(expression: str) -> str:
    """Evalúa una expresión aritmética simple, por ejemplo '23 * 4 + 1'."""
    return calculate(expression)


@mcp.tool()
def clima(ciudad: str) -> str:
    """Devuelve el clima actual (simulado) de una ciudad."""
    return get_clima(ciudad)


@mcp.tool()
def buscar_documentos(consulta: str) -> str:
    """Busca en los documentos cargados con /documents y devuelve los fragmentos más relevantes."""
    results = rag_search(consulta)
    if not results:
        return "No se encontraron documentos relevantes."
    return "\n\n".join(f'[{r["title"]}] {r["text"]}' for r in results)


if __name__ == "__main__":
    mcp.run()
