from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str

API_URL = "https://api-inference.huggingface.co/models/gpt2"
API_TOKEN = "tu_token_de_api_aqui"  # Reemplaza esto con tu token real

headers = {"Authorization": f"Bearer {API_TOKEN}"}

@app.get("/")
async def root():
    return {"message": "Hugging Face API is running"}

@app.post("/generate")
async def generate_text(request: PromptRequest):
    async with httpx.AsyncClient() as client:
        response = await client.post(API_URL, headers=headers, json={"inputs": request.prompt})
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error from Hugging Face API")
    
    return {"generated_text": response.json()[0]["generated_text"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)