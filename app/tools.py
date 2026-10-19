import ast
import operator

_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}


def _eval_node(node):
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.BinOp):
        return _OPS[type(node.op)](_eval_node(node.left), _eval_node(node.right))
    if isinstance(node, ast.UnaryOp):
        return _OPS[type(node.op)](_eval_node(node.operand))
    raise ValueError("Expresión no soportada")


def calculate(expression: str) -> str:
    """Evalúa una expresión aritmética simple de forma segura (sin eval())."""
    try:
        tree = ast.parse(expression, mode="eval")
        return str(_eval_node(tree.body))
    except Exception as exc:
        return f"Error evaluando '{expression}': {exc}"


def get_clima(ciudad: str) -> str:
    # Dato simulado a propósito: en un proyecto real llamarías aquí a una API de clima.
    return f"En {ciudad} hace 22°C y está despejado (dato simulado para el taller)."


TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Evalúa una expresión aritmética, por ejemplo '23 * 4 + 1'.",
            "parameters": {
                "type": "object",
                "properties": {"expression": {"type": "string"}},
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_clima",
            "description": "Devuelve el clima actual de una ciudad.",
            "parameters": {
                "type": "object",
                "properties": {"ciudad": {"type": "string"}},
                "required": ["ciudad"],
            },
        },
    },
]

TOOLS_IMPL = {"calculate": calculate, "get_clima": get_clima}
