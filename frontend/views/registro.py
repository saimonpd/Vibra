import streamlit as st

st.header("Cuestionario de sentimientos")

with st.form("cuestionario_alumno"):
    palabra = st.text_input("¿Que palabra define tus sentimientos ahora mismo?")

    terminado = st.form_submit_button("Enviar")

if terminado:
    # 1. Comprobar que escribió algo
    # 2. Meter dentro de un JSON
    # 3. Llevarlo hacia la API
    # 4. Comprobar la respuesta de la API (excepts)
    # Si se ha enviado correctamente meter un st.warning avisando de que ya ha sido registrado 
    # Si ha habido un error especificarlo.
    pass