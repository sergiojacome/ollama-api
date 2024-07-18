from fastapi import FastAPI
from pydantic import BaseModel
import markovify
import random

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str

# Texto de ejemplo más extenso para entrenar el modelo
text = """
Hola, ¿cómo estás? Espero que te encuentres bien. El día está soleado y agradable.
Me gusta caminar por el parque en días así. La programación es fascinante.
Siempre hay algo nuevo que aprender en el mundo de la tecnología.
¿Qué opinas sobre la inteligencia artificial? Es un tema muy interesante y complejo.
Los avances en machine learning están cambiando muchas industrias.
Me encanta aprender sobre nuevas culturas y viajar a lugares diferentes.
La música tiene el poder de cambiar nuestro estado de ánimo en segundos.
Leer libros es una gran forma de expandir nuestros horizontes y conocimiento.
El ejercicio regular es importante para mantener una buena salud física y mental.
La cocina puede ser una forma creativa de expresión y compartir con amigos y familia.
"""

# Crear el modelo
text_model = markovify.Text(text)

@app.get("/")
async def root():
    return {"message": "Simple text generation API is running"}

@app.post("/generate")
async def generate_text(request: PromptRequest):
    # Generar múltiples oraciones y elegir una al azar
    sentences = [text_model.make_sentence() for _ in range(5)]
    generated = next((s for s in sentences if s is not None), "Lo siento, no pude generar una respuesta.")
    
    # Lista de posibles respuestas iniciales
    greetings = [
        "¡Hola! ",
        "¡Qué tal! ",
        "Buenas, ",
        "Saludos. ",
        "Hey, "
    ]
    
    # Combinar un saludo aleatorio con la oración generada
    response = random.choice(greetings) + generated
    
    return {"generated_text": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)