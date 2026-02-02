from fastapi import APIRouter, UploadFile, File, Form
from app.api.schemas import VisionTextRequest, VisionTextResponse
from app.core.orchestrator import process_request
import json
from app.modules.ocr import list_ocr_models
from app.modules.vision import list_vision_models

router = APIRouter()


@router.post("/analyze", response_model=VisionTextResponse)
async def analyze_image(
    file: UploadFile = File(None),
    base64: str = Form(None),
    request: str = Form(None)
):
    image_bytes = None
    
    # Handle file upload or base64 input
    if file:
        image_bytes = await file.read()
    elif base64:
        import base64 as b64_module
        try:
            # Try to decode base64 string directly
            image_bytes = b64_module.b64decode(base64.split(',')[-1])  # Handle "data:image/..." format
        except Exception as e:
            raise ValueError(f"Invalid base64 string: {str(e)}")
    else:
        raise ValueError("Either 'file' or 'base64' parameter is required")
    
    parsed = None
    if request:
        try:
            parsed = VisionTextRequest.parse_raw(request)
        except Exception:
            try:
                parsed = VisionTextRequest(**json.loads(request))
            except Exception:
                parsed = None

    result = process_request(image_bytes, parsed)
    return result


@router.get("/models")
async def models_available():
    return {"ocr": list_ocr_models(), "vision": list_vision_models()}
