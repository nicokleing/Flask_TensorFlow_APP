# Usar una imagen base de Miniconda
FROM continuumio/miniconda3

# Copiar el archivo environment.yml al directorio de trabajo en el contenedor
COPY environment.yml /app/environment.yml
WORKDIR /app

# Crear el entorno Conda a partir del archivo environment.yml
RUN conda env create -f environment.yml

# Asegurarse de que los comandos se ejecuten dentro del entorno Conda
SHELL ["conda", "run", "-n", "deeplearning", "/bin/bash", "-c"]

# Copiar el resto de la aplicación al directorio de trabajo
COPY . /app

# Exponer el puerto en el que se ejecutará la aplicación
EXPOSE 5000

# El ENTRYPOINT inicia la aplicación dentro del entorno Conda
ENTRYPOINT ["conda", "run", "-n", "deeplearning", "python", "app.py"]



FROM python:3.8-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Expose the port the app runs on
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
