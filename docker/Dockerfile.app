FROM visiontext:latest

# Only replace application code to avoid reinstalling heavy dependencies
WORKDIR /app

# Create cache directories for model caching
RUN mkdir -p /cache/huggingface /cache/torch /cache/easyocr

# Set environment variables for model caching
ENV HF_HOME=/cache/huggingface
ENV TORCH_HOME=/cache/torch
ENV EASYOCR_HOME=/cache/easyocr
ENV PIP_CACHE_DIR=/cache/pip

COPY app ./app
COPY static ./static
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
