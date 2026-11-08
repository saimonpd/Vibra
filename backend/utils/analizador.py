import unicodedata

# Aqui estan las emociones ya conocidas en botones, otras se guardan en otras_emociones.jsonl analizadas
EMOCIONES = {
    "alegre": "positivo",
    "agobiado": "negativo",
    "tranquilo": "positivo",
    "triste": "negativo",
    "indiferente": "neutro",
    "motivado": "positivo",
    "cansado": "negativo",
    "orgulloso": "positivo",
    "enfadado": "negativo",
    "chill": "neutro"
    }


def normalizar(texto: str) -> str:
    """Minúsculas, sin espacios sobrantes y sin tildes (respeta la ñ)."""
    texto = unicodedata.normalize("NFD", texto.strip().lower())
    texto = "".join(
        c for c in texto
        if unicodedata.category(c) != "Mn" or c == "\u0303" 
    )
    return unicodedata.normalize("NFC", texto)


# Las claves pasan por la MISMA función de limpieza que la palabra recibida
_CONOCIDAS = {normalizar(p): s for p, s in EMOCIONES.items()}


def clasificar(palabra: str) -> str:
    """Devuelve 'positivo', 'neutro', 'negativo' o 'pendiente' si aún no se sabe."""
    return _CONOCIDAS.get(normalizar(palabra), "pendiente")
    # Aquí, más adelante: si no está en el diccionario, llamar a la IA.
