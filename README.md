# VisionText

Modular OCR & Vision API scaffold.

Project layout
--------------

- `app/` - application source code
	- `main.py` - FastAPI app and startup configuration
	- `api/` - API router, routes and request/response schemas
	- `core/` - orchestrator and core utilities for processing requests
	- `modules/` - pluggable modules (OCR and vision backends)
		- `ocr/` - OCR engines and factory (Tesseract, EasyOCR)
		- `vision/` - vision models (BLIP, etc.)
	- `utils/` - helper utilities (image loaders, file helpers)

- `docker/` - Dockerfiles and helper scripts for building images
- `models/` - (optional) local model snapshots and cached files
- `static/` - static UI assets (simple test page)
- `requirements.txt` - Python dependencies for the application

Quick start (local)
-------------------

1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate   # Unix/macOS
.venv\\Scripts\\Activate.ps1 # Windows PowerShell
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the API server in development mode:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Docker (CPU build)
------------------

### Using Docker Compose (recommended)

```bash
docker-compose up -d

# API at http://localhost:8000
# UI at http://localhost:8000/ui
# Models cached in Docker Volume
```

**For Coolify Deployment:** Use `docker-compose.production.yml` instead!
See [DOCKER_SETUP.md](DOCKER_SETUP.md#coolify-deployment) for details.

### Manual Docker Build
$env:DOCKER_BUILDKIT=1
docker build -t visiontext:app-cpu -f docker/Dockerfile.cpu .
```

Run the container:

```powershell
docker run -d -p 8000:8000 --name visiontext_app --rm -e TRANSFORMERS_OFFLINE=1 visiontext:app-cpu
```

Docker (optional GPU build)
---------------------------

If you need a GPU-enabled image, use a CUDA base image and install matching CUDA-aware wheels (for example PyTorch). The repository contains `docker/Dockerfile.gpu` as a template — pick a CUDA version compatible with your host drivers and the wheels you plan to install.

Notes
-----

- The project uses a pluggable architecture for OCR engines and vision models. Add or remove backends in `app/modules/`.
- Large model files may be preloaded during Docker builds into the `/app/models` directory. Keep an eye on image size if you bake many models into the image.

Troubleshooting
---------------

- If the API fails to start, check container logs with `docker logs <container>`.
- If you need GPU support, ensure the base image, host drivers, and Python wheel tags (CUDA version) all match.

