from fastapi import FastAPI
from pydantic import BaseModel
import markovify

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str

# Texto de ejemplo para entrenar el modelo
text = """
Hola, ¿cómo estás? Espero que te encuentres bien.
El día está soleado y agradable. Me gusta caminar por el parque en días así.
La programación es fascinante. Siempre hay algo nuevo que aprender.
¿Qué opinas sobre la inteligencia artificial? Es un tema muy interesante.
"""

# Crear el modelo
text_model = markovify.Text(text)

@app.get("/")
async def root():
    return {"message": "Simple text generation API is running"}

@app.post("/generate")
async def generate_text(request: PromptRequest):
    # Generar una oración basada en el prompt
    generated = text_model.make_short_sentence(max_chars=100)
    return {"generated_text": f"{request.prompt} {generated}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)