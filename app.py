import streamlit as st
import requests
import pandas as pd

# Función para dar formato de consola al texto
def generar_reporte_texto(texto_original, data):
    separador = "=" * 70 + "\n"
    reporte = ""

    # ──────────────────────────────────────────────
    # Etapa 1
    # ──────────────────────────────────────────────
    reporte += separador
    reporte += "ETAPA 1: SEGMENTACIÓN EN FRASES (Sentence Segmentation)\n"
    reporte += separador + "\n"
    reporte += "Comentario: El texto original no contiene signos de puntuación.\n"
    reporte += "spaCy utiliza su modelo neuronal basado en el dependency parser para\n"
    reporte += "predecir los límites oracionales a partir de patrones sintácticos y\n"
    reporte += "relaciones de dependencia entre palabras, incluso en ausencia de\n"
    reporte += "puntos, comas u otros delimitadores explícitos.\n\n"
    for i, frase in enumerate(data["frases"], 1):
        reporte += f"  Frase {i}: {frase}\n"
    reporte += "\n"

    # ──────────────────────────────────────────────
    # Etapa 2
    # ──────────────────────────────────────────────
    reporte += separador
    reporte += "ETAPA 2: TOKENIZACIÓN (Tokens)\n"
    reporte += separador + "\n"
    reporte += f"  Total de tokens: {data['total_tokens']}\n\n"
    
    # Extraemos solo los textos de los tokens para la lista
    lista_tokens = [item["token"] for item in data["detalles_tokens"]]
    reporte += f"  Tokens: {lista_tokens}\n\n"

    # ──────────────────────────────────────────────
    # Etapa 3
    # ──────────────────────────────────────────────
    reporte += separador
    reporte += "ETAPA 3: LEMATIZACIÓN (Lemmas)\n"
    reporte += separador + "\n"
    reporte += f"  {'TOKEN':<20} {'LEMA':<20}\n"
    reporte += f"  {'-----':<20} {'-----':<20}\n"
    for item in data["detalles_tokens"]:
        reporte += f"  {item['token']:<20} {item['lema']:<20}\n"
    reporte += "\n"

    # ──────────────────────────────────────────────
    # Etapa 4
    # ──────────────────────────────────────────────
    reporte += separador
    reporte += "ETAPA 4: POS TAGGING (Etiquetado Gramatical)\n"
    reporte += separador + "\n"
    reporte += f"  {'TOKEN':<20} {'POS':<12} {'ETIQUETA':<12}\n"
    reporte += f"  {'-----':<20} {'---':<12} {'--------':<12}\n"
    for item in data["detalles_tokens"]:
        reporte += f"  {item['token']:<20} {item['pos']:<12} {item['tag']:<12}\n"
    reporte += "\n"

    # ──────────────────────────────────────────────
    # Etapa 5
    # ──────────────────────────────────────────────
    reporte += separador
    reporte += "ETAPA 5: FILTRADO DE STOPWORDS\n"
    reporte += separador + "\n"
    reporte += f"  Texto original: {texto_original}\n\n"
    reporte += f"  Texto sin stopwords: {data['texto_limpio']}\n\n"

    return reporte


# ──────────────────────────────────────────────
# Interfaz de Streamlit
# ──────────────────────────────────────────────
st.set_page_config(page_title="NLP Pipeline", layout="wide")
st.title("⚙️ Pipeline de NLP con spaCy")

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
                    # Filtramos las columnas para mostrarlas mejor en la tabla visual
                    st.dataframe(df[["token", "lema", "pos", "tag"]], use_container_width=True)
                
                # --- NUEVA SECCIÓN: BOTÓN DE DESCARGA ---
                st.markdown("---")
                st.subheader("📥 Exportar Resultados")
                
                # Generamos el texto con el formato solicitado
                texto_descarga = generar_reporte_texto(texto_input, data)
                
                # Botón nativo de descarga de Streamlit
                st.download_button(
                    label="Descargar Reporte en formato .txt",
                    data=texto_descarga,
                    file_name="reporte_pipeline_nlp.txt",
                    mime="text/plain"
                )
                
            else:
                st.error(f"Error HTTP: {response.status_code}")
                st.write("Detalle del error devuelto por la API:", response.text)
        except requests.exceptions.ConnectionError:
            st.error("No se pudo conectar con la API. Verifica que el backend esté corriendo y la URL sea correcta.")
