import streamlit as st
import requests
import os
from dotenv import load_dotenv
from utils.lista_emociones import emociones

load_dotenv()

API_URL = os.environ.get("API_URL")

st.header("Cuestionario de sentimientos")

with st.form("cuestionario_alumno"):

    seleccionador_emociones = st.pills(
        "¿Que palabra define tus sentimientos ahora mismo?",
        options=emociones.keys(),
        format_func=lambda option: emociones[option],
        selection_mode="single"
    )

    palabra = st.text_input("Otra: (Si escribes aqui, lo seleccionado arriba no contara.)")
# (Futuro) Si la API no esta disponible -> guardar palabra y fecha en lista + avisar al usuario -> cuando este la API disponile continuar el proceso

api_disponible = False
try:
    estado_API = requests.get(
        f"{API_URL}/salud",
        timeout=5
    )
    if estado_API.status_code == 200:
        api_disponible = True
except requests.exceptions.RequestException as error:
    print(f"La api de salud ha dado error: {error}")

if api_disponible:
    with st.form("cuestionario_alumno"):
        palabra = st.text_input("¿Que palabra define tus sentimientos ahora mismo?")

        terminado = st.form_submit_button("Enviar")

    if terminado:
        # Si 'palabra' es un string, le quitamos los espacios. Si es None o no es string, queda como ""
        palabra_limpia = palabra.strip() if isinstance(palabra,str) else ""
        if seleccionador_emociones is None and palabra_limpia == "":
            st.warning("Para enviar tienes que seleccionar una emocion o escribir algo.")
        else:
            if palabra_limpia:
                palabra_a_enviar = palabra_limpia
            elif seleccionador_emociones is not None:
                palabra_a_enviar = emociones[seleccionador_emociones]
            try:
                respuesta = requests.post(
                    f"{API_URL}/palabras",
                    json={"palabra": palabra_a_enviar},
                    timeout=5,
                )
                if respuesta.status_code == 200:
                    st.success(f"¡Gracias por tu respuesta!")

                else:
                    st.error(f"Ha habido un error en el servidor, intentalo de nuevo.")
                    print(f"Ha habido un error en el servidor: {respuesta.text}")
            except requests.exceptions.RequestException as error:
                st.error(f"Nuestro servicio no esta disponible ahora, intentalo de nuevo o ponte en contacto con nosotros")
                print(f"No se pudo conectar con la API: {error}")

else:
    st.write("No hemos podido cargar el formulario porque uno de nuestros servicios internos no esta funcionando correctamente.")
    st.write("Avisa al responsable o intentalo mas tarde")
