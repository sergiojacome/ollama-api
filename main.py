from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str

@app.get("/")
async def root():
    return {"message": "Ollama API is running"}

@app.post("/generate")
async def generate_text(request: PromptRequest):
    # Simular una respuesta en lugar de usar Ollama
    return {"generated_text": f"Respuesta simulada a: {request.prompt}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)