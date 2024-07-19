import subprocess
import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str

# Iniciar Ollama como un proceso separado
ollama_process = subprocess.Popen(["/app/ollama", "serve"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Esperar a que Ollama se inicie completamente
time.sleep(10)  # Ajusta este tiempo según sea necesario

# Descargar el modelo (esto puede tardar un tiempo)
try:
    subprocess.run(["/app/ollama", "pull", "orca-mini"], check=True, timeout=600)
except subprocess.CalledProcessError as e:
    print(f"Error al descargar el modelo: {e}")
except subprocess.TimeoutExpired:
    print("Timeout al descargar el modelo")

@app.get("/")
async def root():
    return {"message": "Ollama API is running"}

@app.post("/generate")
async def generate_text(request: PromptRequest):
    try:
        result = subprocess.run(
            ["/app/ollama", "run", "orca-mini", request.prompt],
            capture_output=True,
            text=True,
            check=True,
            timeout=60  # Aumentar el timeout para dar más tiempo a la generación
        )
        return {"generated_text": result.stdout.strip()}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Error al generar texto: {e.stderr}")
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail="Timeout al generar texto")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)