import os

import requests
import streamlit as st
from dotenv import load_dotenv

from utils.grafico_nube import generar_nube

load_dotenv()
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")
MIN_PALABRAS = 5  # por debajo de esto la nube se ve pobre


def obtener_conteo() -> list[dict] | None:
    """Devuelve la lista del backend, o None si no se pudo obtener."""
    try:
        respuesta = requests.get(f"{API_URL}/conteo", timeout=5)
        respuesta.raise_for_status()  # convierte 4xx/5xx en excepción
        return respuesta.json()
    except requests.exceptions.RequestException:
        return None


st.title("☁️ Nube de palabras")

conteo = obtener_conteo()

if conteo is None:
    st.error("El servicio no está disponible ahora mismo. Inténtalo en unos minutos.")
elif len(conteo) == 0:
    st.info("Todavía no hay palabras registradas.")
else:
    total = sum(fila["cantidad"] for fila in conteo)
    if total < MIN_PALABRAS:
        st.caption(f"Solo hay {total} respuestas: la nube mejorará cuando haya más.")

    figura = generar_nube(conteo)

    st.pyplot(figura)
    st.caption(f"Total de respuestas: {total}  ·  🟢 Positivo  ⚪ Neutro  🔴 Negativo")