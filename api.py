from fastapi import FastAPI
from pydantic import BaseModel
import spacy

app = FastAPI(title="NLP Pipeline API")

# Cargar el modelo en español
nlp = spacy.load("es_core_news_sm")

# Esquema de datos para recibir el texto
class TextRequest(BaseModel):
    text: str

@app.post("/analyze")
def analyze_text(req: TextRequest):
    doc = nlp(req.text)
    
    # Etapa 1: Frases
    frases = [sent.text for sent in doc.sents]
    
    # Etapa 2: Tokens
    tokens = [token.text for token in doc]
    
    # Etapa 3 y 4: Lematización y POS
    detalles = []
    for token in doc:
        detalles.append({
            "token": token.text,
            "lema": token.lemma_,
            "pos": token.pos_,
            "tag": token.tag_
        })
        
    # Etapa 5: Stopwords
    tokens_sin_stopwords = [token.text for token in doc if not token.is_stop]
    texto_limpio = " ".join(tokens_sin_stopwords)
    
    return {
        "frases": frases,
        "total_tokens": len(tokens),
        "detalles_tokens": detalles,
        "texto_limpio": texto_limpio
    }