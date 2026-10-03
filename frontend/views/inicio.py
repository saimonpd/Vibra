import streamlit as st

st.title("👋 Hola, ")
st.subheader("¿Cómo te ha ido el día?")
st.text("" \
"Vibra es una pequeña aplicación donde cada persona de la clase resume en una sola palabra cómo se siente. " \
"Con las palabras de todos, construimos entre todos una imagen de cómo está el grupo.")
st.divider()
st.subheader("🎯 Nuestro objetivo")
st.text("A veces se nota el ambiente en clase, pero pocas veces hablamos de él. Con Vibra queremos:")
st.text("- Dar voz a todos, también a quien no suele hablar en voz alta.")
st.text("- Ver cómo evoluciona el ánimo de la clase día a día.")
st.text("- Detectar a tiempo cuándo conviene parar y hablar de cómo estamos.")
st.divider()
st.subheader("⚙️ Cómo funciona")
st.text("1. Escribes una palabra en la página de cuestionario")
st.text("2. Una IA analiza si estas expresando un sentimiento positivo, neutro o negativo")
st.text("3. Aparece en las estadísticas, mezcladas con el resto de la clase.")
st.divider()
st.subheader("🔒 Tu palabra es anónima. No guardamos quién la escribe.")
col1, col2 = st.columns(2)
with col1:
    st.page_link("views/registro.py", label="Haz el cuestionario anonimo", icon="📝")
with col2:
    st.page_link("views/estadisticas.py", label="Mira las estadisticas de la clase", icon="📊")