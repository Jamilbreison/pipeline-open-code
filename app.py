import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="NLP Pipeline", layout="wide")
st.title("⚙️ Pipeline de NLP con spaCy")

# IMPORTANTE: Cambia esta URL por la que te dé Render una vez desplegado el backend
API_URL = "https://pipeline-open-code.onrender.com/analyze"

texto_input = st.text_area(
    "Ingresa el texto a analizar:",
    "Netflix ha encontrado en el juego del calamar su nuevo fenómeno mundial..."
)

if st.button("Ejecutar Pipeline"):
    with st.spinner("Procesando en el backend..."):
        try:
            response = requests.post(API_URL, json={"text": texto_input})
            
            if response.status_code == 200:
                data = response.json()
                
                st.subheader("Etapa 1: Segmentación en Frases")
                for i, frase in enumerate(data["frases"], 1):
                    st.info(f"**Frase {i}:** {frase}")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("Etapa 2: Tokens")
                    st.write(f"**Total de tokens:** {data['total_tokens']}")
                    
                    st.subheader("Etapa 5: Filtrado de Stopwords")
                    st.success(data["texto_limpio"])
                    
                with col2:
                    st.subheader("Etapas 3 y 4: Lematización y POS")
                    df = pd.DataFrame(data["detalles_tokens"])
                    st.dataframe(df, use_container_width=True)
                    
            else:
                st.error(f"Error HTTP: {response.status_code}")
                st.write("Detalle del error devuelto por la API:", response.text)
        except requests.exceptions.ConnectionError:
            st.error("No se pudo conectar con la API. Verifica que el backend esté corriendo y la URL sea correcta.")
