from mcp.server.mcpserver import MCPServer

from app.tools import calculate, get_clima
from app.rag import search as rag_search
from app.sheets_client import append_row

mcp = MCPServer("workshop-tools")


@mcp.tool()
def calcular(expression: str) -> str:
    """Evalúa una expresión aritmética simple, por ejemplo '23 * 4 + 1'."""
    return calculate(expression)


@mcp.tool()
def clima(ciudad: str) -> str:
    """Devuelve el clima actual real de una ciudad (Open-Meteo)."""
    return get_clima(ciudad)


@mcp.tool()
def buscar_documentos(consulta: str) -> str:
    """Busca en los documentos cargados con /documents y devuelve los fragmentos más relevantes."""
    results = rag_search(consulta)
    if not results:
        return "No se encontraron documentos relevantes."
    return "\n\n".join(f'[{r["title"]}] {r["text"]}' for r in results)


@mcp.tool()
def agregar_fila_sheet(spreadsheet_id: str, valores: list[str]) -> str:
    """Agrega una fila al final de una hoja de Google Sheets. `valores` es la lista de celdas de la fila."""
    return append_row(spreadsheet_id, valores)


if __name__ == "__main__":
    mcp.run()
