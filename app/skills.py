SKILLS = [
    {
        "name": "resumen",
        "keywords": ["resume", "resumir", "resumen"],
        "instructions": (
            "Actúa como un asistente de resúmenes. Responde en máximo 3 "
            "viñetas, en español, sin agregar opiniones ni información que "
            "no esté en el texto del usuario."
        ),
    },
    {
        "name": "traductor",
        "keywords": ["traduce", "traducir", "traducción", "to english", "al inglés"],
        "instructions": (
            "Actúa como traductor. Traduce el mensaje del usuario al idioma "
            "que pida (o a inglés si no especifica) y responde SOLO con la "
            "traducción, sin explicaciones adicionales."
        ),
    },
    {
        "name": "code-review",
        "keywords": ["revisa este código", "code review", "revisar código", "bug en mi código"],
        "instructions": (
            "Actúa como revisor de código senior. Señala errores y riesgos "
            "de seguridad, y propone una mejora concreta. Responde en "
            "formato de lista."
        ),
    },
]


def select_skill(message: str) -> dict | None:
    lowered = message.lower()
    for skill in SKILLS:
        if any(keyword in lowered for keyword in skill["keywords"]):
            return skill
    return None
