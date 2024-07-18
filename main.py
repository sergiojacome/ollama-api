from fastapi import FastAPI
from pydantic import BaseModel
import ollama

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str

@app.post("/generate")
async def generate_text(request: PromptRequest):
    response = ollama.generate(model='llama2', prompt=request.prompt)
    return {"generated_text": response['response']}