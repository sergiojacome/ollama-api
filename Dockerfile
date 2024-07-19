FROM python:3.9-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Descargar Ollama pre-compilado
RUN curl -L https://github.com/jmorganca/ollama/releases/download/v0.1.27/ollama-linux-amd64 -o ollama \
    && chmod +x ollama

# Copiar los archivos de la aplicación
COPY requirements.txt .
COPY app.py .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]