from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import os

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str

@app.post("/generate")
async def generate_text(request: PromptRequest):
    try:
        # Inicia el servidor Ollama si no está en ejecución
        subprocess.Popen(["/app/ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Ejecuta el comando Ollama
        result = subprocess.run(
            ["/app/ollama", "run", "distilbert", request.prompt],
            capture_output=True,
            text=True,
            check=True
        )
        return {"generated_text": result.stdout.strip()}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Error al generar texto: {e.stderr}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)