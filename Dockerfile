# Usamos Python 3.10 slim (ligero)
FROM python:3.10-slim

# Instalar dependencias del sistema que necesita psycopg2
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar dependencias primero (para aprovechar caché de Docker)
COPY pyproject.toml ./

# Instalar dependencias de Python
RUN pip install --no-cache-dir -e ".[dev]"

# Copiar TODO el código del proyecto
COPY . .

# Puerto que expone FastAPI
EXPOSE 8000

# Comando por defecto (lo sobrescribiremos en docker-compose)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]