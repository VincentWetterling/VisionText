from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api.routes import router
import logging
import warnings
import os

# Reduce noisy logs from third-party libs (transformers/huggingface, torch, easyocr)
# Set environment flags to reduce HF telemetry and make transformers quieter when possible
os.environ.setdefault('HF_HUB_DISABLE_TELEMETRY', '1')
os.environ.setdefault('TRANSFORMERS_NO_ADVISORY_WARNINGS', '1')

# Configure Python logging levels for noisy libraries
logging.getLogger('uvicorn.error').setLevel(logging.INFO)
logging.getLogger('transformers').setLevel(logging.WARNING)
logging.getLogger('huggingface_hub').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)
logging.getLogger('filelock').setLevel(logging.WARNING)
logging.getLogger('easyocr').setLevel(logging.WARNING)

# Transformers offers a utility to set verbosity; try to silence info-level messages
try:
    from transformers import logging as transformers_logging
    transformers_logging.set_verbosity_error()
except Exception:
    pass

# Filter known noisy warnings coming from torch
warnings.filterwarnings('ignore', message="No ccache found.*")
warnings.filterwarnings('ignore', message="'pin_memory' argument is set as true but no accelerator is found.*")
warnings.filterwarnings('ignore', message="The image processor of type.*is now loaded as a fast processor by default.*")

app = FastAPI(
    title="VisionText",
    description="Modular OCR & Vision API",
    version="0.1.0"
)

# Allow local frontends to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Determine static directory
if os.path.exists('/app/static'):
    static_dir = '/app/static'
else:
    static_dir = os.path.join(os.path.dirname(__file__), '..', 'static')

# Serve all static files
app.mount('/static', StaticFiles(directory=static_dir), name='static')

# Serve UI HTML directly
@app.get('/ui')
@app.get('/ui/')
async def serve_ui():
    html_file = os.path.join(static_dir, 'model_test.html')
    if os.path.exists(html_file):
        return FileResponse(html_file, media_type='text/html')
    return {'detail': 'UI not found'}

app.include_router(router)
