from fastapi import FastAPI
import ollama

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Ollama API is running"}

@app.post("/generate")
async def generate_text(prompt: str):
    response = ollama.generate(model='llama2', prompt=prompt)
    return {"generated_text": response['response']}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)