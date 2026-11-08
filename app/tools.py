import ast
import operator

import requests

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


_WEATHER_CODES = {
    0: "despejado",
    1: "mayormente despejado",
    2: "parcialmente nublado",
    3: "nublado",
    45: "con niebla",
    48: "con niebla y escarcha",
    51: "con llovizna ligera",
    53: "con llovizna",
    55: "con llovizna densa",
    61: "con lluvia ligera",
    63: "con lluvia",
    65: "con lluvia fuerte",
    71: "con nevada ligera",
    73: "con nevada",
    75: "con nevada fuerte",
    80: "con chubascos ligeros",
    81: "con chubascos",
    82: "con chubascos fuertes",
    95: "con tormenta eléctrica",
}


def get_clima(ciudad: str) -> str:
    """Clima actual real, vía Open-Meteo (geocoding + forecast, sin API key)."""
    geo = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": ciudad, "count": 1, "language": "es", "format": "json"},
        timeout=10,
    ).json()
    results = geo.get("results")
    if not results:
        return f"No encontré la ciudad '{ciudad}'."

    lugar = results[0]
    forecast = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": lugar["latitude"],
            "longitude": lugar["longitude"],
            "current_weather": "true",
        },
        timeout=10,
    ).json()
    actual = forecast.get("current_weather", {})
    temperatura = actual.get("temperature")
    descripcion = _WEATHER_CODES.get(actual.get("weathercode"), "condición desconocida")

    return f"En {lugar['name']} hace {temperatura}°C y está {descripcion} (datos en vivo de Open-Meteo)."


def send_email(to: str, subject: str, body: str) -> str:
    """Envía un correo real por Gmail API (requiere credentials/gmail_token.json, ver tutorial)."""
    from .email_client import send_gmail

    return send_gmail(to=to, subject=subject, body=body)


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
            "description": "Devuelve el clima actual real de una ciudad (Open-Meteo).",
            "parameters": {
                "type": "object",
                "properties": {"ciudad": {"type": "string"}},
                "required": ["ciudad"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "send_email",
            "description": "Envía un correo real por Gmail a un destinatario, con asunto y cuerpo.",
            "parameters": {
                "type": "object",
                "properties": {
                    "to": {"type": "string", "description": "Correo del destinatario"},
                    "subject": {"type": "string"},
                    "body": {"type": "string"},
                },
                "required": ["to", "subject", "body"],
            },
        },
    },
]

TOOLS_IMPL = {"calculate": calculate, "get_clima": get_clima, "send_email": send_email}
