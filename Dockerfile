# Usar una imagen ligera oficial de Python
FROM python:3.10-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalar dependencias del sistema necesarias para compilar ciertas librerías
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar el archivo de requerimientos e instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el script del pipeline al contenedor
COPY pipeline_paralelo.py .

# Comando de ejecución por defecto al levantar el contenedor
CMD ["python", "pipeline_paralelo.py"]