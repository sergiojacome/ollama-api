from fastapi import FastAPI
from pydantic import BaseModel
import markovify
import random

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str

# Texto de entrenamiento ampliado
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
El aprendizaje continuo es clave para el crecimiento personal y profesional.
La naturaleza tiene mucho que enseñarnos sobre equilibrio y adaptación.
Las redes sociales han cambiado la forma en que nos comunicamos e interactuamos.
El trabajo en equipo es fundamental para lograr grandes objetivos.
La innovación surge a menudo de la necesidad de resolver problemas cotidianos.
"""

# Crear el modelo
text_model = markovify.Text(text)

@app.get("/")
async def root():
    return {"message": "Simple text generation API is running"}

@app.post("/generate")
async def generate_text(request: PromptRequest):
    # Intentar generar una oración corta
    generated = text_model.make_short_sentence(max_chars=60)
    
    # Si no se pudo generar, usar una respuesta predeterminada
    if not generated:
        responses = [
            "Estoy bien, gracias por preguntar.",
            "Todo va genial por aquí.",
            "Muy bien, ¿y tú qué tal?",
            "Excelente, espero que tú también.",
            "Bien, aunque siempre hay espacio para mejorar."
        ]
        generated = random.choice(responses)
    
    # Lista de posibles respuestas iniciales
    greetings = [
        "¡Hola! ",
        "¡Qué tal! ",
        "Buenas, ",
        "Saludos. ",
        "Hey, "
    ]
    
    # Combinar un saludo aleatorio con la respuesta generada o predeterminada
    response = random.choice(greetings) + generated
    
    return {"generated_text": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)