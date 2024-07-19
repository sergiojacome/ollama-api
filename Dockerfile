FROM python:3.9-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Clonar Ollama
RUN git clone https://github.com/jmorganca/ollama.git

# Instalar Go 1.22
RUN curl -OL https://go.dev/dl/go1.22.0.linux-amd64.tar.gz \
    && tar -C /usr/local -xzf go1.22.0.linux-amd64.tar.gz \
    && rm go1.22.0.linux-amd64.tar.gz

# Añadir Go al PATH
ENV PATH=$PATH:/usr/local/go/bin

# Compilar Ollama
WORKDIR /app/ollama
RUN go version && go build

# Volver al directorio de trabajo principal
WORKDIR /app

# Copiar los archivos de la aplicación
COPY requirements.txt .
COPY app.py .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]