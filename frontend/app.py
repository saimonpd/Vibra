import streamlit as st

# Configuracion global de pagina
st.set_page_config(
    page_title="Vibra",
    page_icon="🌱",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Paginas y rutas
pagina_inicio = st.Page("views/inicio.py", title="Inicio", icon="👋", default=True)
pagina_registro = st.Page("views/registro.py", title="Cuestionario", icon="📝")
pagina_estadisticas = st.Page("views/estadisticas.py", title="Estadisticas", icon="📊")

# Menu de Navegacion
pg = st.navigation(
    {
        "Menu Principal": [pagina_inicio, pagina_registro],
        "Informacion": [pagina_estadisticas]     
    }
)
pg.run()