ARG BUILD_TARGET=cpu
ARG BASE_IMAGE=python:3.11-slim
FROM ${BASE_IMAGE}

# system deps for OCR / vision libraries
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    ffmpeg \
    git \
    build-essential \
    cmake \
    wget \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Use an image-stable location for HF caches so models downloaded at build
# time are baked into the image and persist across container restarts.
ENV PIP_NO_CACHE_DIR=0
ENV PIP_DEFAULT_TIMEOUT=100
ENV HF_HOME=/app/models/huggingface
ENV TRANSFORMERS_CACHE=/app/models/huggingface/transformers
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# create the directory early so downloads are stored in image layers
RUN mkdir -p /app/models/huggingface

# Copy requirements and install Python deps.
#
# Build-time options:
# - By default this Dockerfile builds a CPU image using the default
#   base image (python:3.11-slim). To build a GPU image use a CUDA base
#   image and pass build-args, for example:
#
#   docker build \
#     --build-arg BASE_IMAGE=nvidia/cuda:12.2.1-cudnn8-runtime-ubuntu22.04 \
#     --build-arg BUILD_TARGET=gpu \
#     -t visiontext:app -f docker/Dockerfile .
#
# Note: this just selects a GPU-capable base image; installing CUDA-aware
# wheels (PyTorch/CUDA) usually also requires choosing the correct wheel
# and may require extra-index or wheel URLs. Native, platform-specific
# wheels are intentionally handled outside of this generic requirements
# file to avoid installing incompatible binary packages during build.

COPY requirements.txt .

# Install CPU PyTorch wheels first (official CPU index). If this index is
# unavailable for a particular platform, the fallback pip install will try
# the default index which may provide a CPU wheel.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=cache,target=/root/.cache/pip/http \
    pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu \
        "torch" "torchvision" "torchaudio" || \
    pip install --no-cache-dir "torch" "torchvision" "torchaudio" || true

# Install the remaining Python requirements
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=cache,target=/root/.cache/pip/http \
    pip install --cache-dir /root/.cache/pip -r requirements.txt

# copy optional preload script and run at build time to cache models into /app/models/huggingface
COPY docker/preload_models.py /preload_models.py
# Run the preloader without a BuildKit cache mount so downloaded files end up in the image
RUN python /preload_models.py || true

COPY app ./app
# Copy static assets so FastAPI StaticFiles can serve the UI
COPY static ./static
COPY docker/healthcheck.py /healthcheck.py

# Ensure app is importable
RUN python -c "from app.main import app; print('✓ app.main imported successfully')" || true

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
