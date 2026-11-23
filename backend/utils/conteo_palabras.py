from collections import Counter

from pydantic import BaseModel

from database.repository.palabras_repository import RepositorioPalabras


class ConteoPalabra(BaseModel):
    """Una fila del resultado: una palabra con su sentimiento y cuántas veces se repite."""
    palabra: str
    sentimiento: str
    cantidad: int
    fecha: str  # fecha del último registro de esa palabra


def conteo_palabras(repo: RepositorioPalabras, dia: str | None = None) -> list[ConteoPalabra]:
    """1. Pide los registros al repositorio. 2. Los cuenta. 3. Devuelve el resultado."""
    registros = repo.obtener_por_dia(dia)
    return _contar_palabras(registros)


def _contar_palabras(registros: list[dict]) -> list[ConteoPalabra]:
    contador = Counter((r["palabra"], r["sentimiento"]) for r in registros)

    ultima_fecha: dict[tuple[str, str], str] = {}
    for r in registros:
        clave = (r["palabra"], r["sentimiento"])
        ultima_fecha[clave] = max(ultima_fecha.get(clave, ""), r["fecha"])

    return [
        ConteoPalabra(
            palabra=palabra,
            sentimiento=sentimiento,
            cantidad=cantidad,
            fecha=ultima_fecha[(palabra, sentimiento)],
        )
        for (palabra, sentimiento), cantidad in contador.most_common()
    ]