from collections import Counter

import numpy as np
from matplotlib.figure import Figure
from wordcloud import WordCloud

COLORES = {
    "positivo": "#2e7d32",
    "neutro": "#757575",
    "negativo": "#c62828",
}
COLOR_POR_DEFECTO = "#000000"


def _crear_mascara_circular(tamano: int = 400, radio: int = 180) -> np.ndarray:
    """Círculo: en la máscara, 255 (blanco) = zona prohibida, 0 = zona donde se dibuja."""
    x, y = np.ogrid[:tamano, :tamano]
    centro = tamano // 2
    fuera_del_circulo = (x - centro) ** 2 + (y - centro) ** 2 > radio**2
    return 255 * fuera_del_circulo.astype(int)


def generar_nube(conteo: list[dict]) -> Figure:
    """Recibe el JSON de /conteo y devuelve una figura de matplotlib lista para mostrar."""
    # Una palabra puede venir con dos sentimientos distintos, pero WordCloud
    # necesita UNA frecuencia y UN color por palabra:
    # sumamos las cantidades y nos quedamos con el sentimiento más repetido.
    frecuencias: Counter = Counter()
    mejor_sentimiento: dict[str, tuple[int, str]] = {}  # palabra -> (cantidad, sentimiento)

    for fila in conteo:
        palabra, cantidad = fila["palabra"], fila["cantidad"]
        frecuencias[palabra] += cantidad
        if cantidad > mejor_sentimiento.get(palabra, (0, ""))[0]:
            mejor_sentimiento[palabra] = (cantidad, fila["sentimiento"])

    def color_func(word, **kwargs):
        sentimiento = mejor_sentimiento.get(word, (0, ""))[1]
        return COLORES.get(sentimiento, COLOR_POR_DEFECTO)

    nube = WordCloud(
        background_color="white",
        mask=_crear_mascara_circular(),
        color_func=color_func,
    ).generate_from_frequencies(frecuencias)

    # Figure() directo, sin plt: no usa estado global, así que dos usuarios
    # a la vez no se pisan y no hay que acordarse de cerrar la figura.
    fig = Figure(figsize=(7, 7))
    ax = fig.subplots()
    ax.imshow(nube, interpolation="bilinear")
    ax.axis("off")
    return fig