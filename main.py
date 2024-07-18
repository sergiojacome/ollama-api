from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str

# Inicializa el generador de texto
generator = pipeline('text-generation', model='distilgpt2')

@app.get("/")
async def root():
    return {"message": "Local text generation API is running"}

@app.post("/generate")
async def generate_text(request: PromptRequest):
    result = generator(request.prompt, max_length=50, num_return_sequences=1)
    return {"generated_text": result[0]['generated_text']}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)