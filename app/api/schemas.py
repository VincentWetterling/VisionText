from pydantic import BaseModel
from typing import List, Optional

class VisionTextRequest(BaseModel):
    ocr_models: Optional[List[str]] = []
    vision_models: Optional[List[str]] = []
    combine: bool = False

class VisionTextResponse(BaseModel):
    ocr_results: dict
    vision_results: dict
