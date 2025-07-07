FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

# Sistema base
RUN apt update && apt install -y \
    python3 python3-pip ffmpeg git wget unzip curl nano \
    && apt clean

# Crear carpeta de trabajo
WORKDIR /app

# ✅ Clonar DiffRhythm directamente
RUN git clone https://github.com/ASLP-lab/DiffRhythm /app/DiffRhythm

# Copiar solo tus archivos (app.py, Dockerfile, templates, etc.)
COPY app.py /app/app.py
COPY requirements.txt /app/requirements.txt
COPY templates /app/templates

# Instalar dependencias
RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
RUN pip3 install -r requirements.txt
RUN pip3 install flask einops accelerate transformers

# Descargar modelos desde Hugging Face la primera vez que corras
ENV HF_HUB_DISABLE_SYMLINKS_WARNING=1

# Puerto para la API Flask
EXPOSE 8080

CMD ["python3", "app.py"]
