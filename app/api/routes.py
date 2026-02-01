from fastapi import APIRouter, UploadFile, File, Form
from app.api.schemas import VisionTextRequest, VisionTextResponse
from app.core.orchestrator import process_request
import json
from app.modules.ocr import list_ocr_models
from app.modules.vision import list_vision_models

router = APIRouter()


@router.post("/analyze", response_model=VisionTextResponse)
async def analyze_image(
    file: UploadFile = File(...),
    request: str = Form(None)
):
    image_bytes = await file.read()
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
