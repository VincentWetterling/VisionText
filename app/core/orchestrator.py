from app.modules.ocr import get_ocr_module
from app.modules.vision import get_vision_module
from app.utils.image import load_image

def _sanitize_value(v):
    try:
        import numpy as _np
    except Exception:
        _np = None

    # numpy arrays -> convert to list
    if _np is not None and isinstance(v, _np.ndarray):
        return v.tolist()

    # numpy generic scalars (e.g., numpy.int32/float64)
    if _np is not None and isinstance(v, _np.generic):
        return v.item()

    # basic types (str before iterable checks so strings aren't expanded)
    if isinstance(v, (str, int, float, bool)) or v is None:
        return v

    # dict -> sanitize items
    if isinstance(v, dict):
        return {k: _sanitize_value(val) for k, val in v.items()}

    # list/tuple -> sanitize elements
    if isinstance(v, (list, tuple)):
        return [_sanitize_value(x) for x in v]

    # fallback: try to convert to str for unknown types
    try:
        return str(v)
    except Exception:
        return None

def process_request(image_bytes, request):
    image = load_image(image_bytes)

    ocr_results = {}
    vision_results = {}

    # safeguard if request is None
    if request is None:
        request = type("R", (), {"ocr_models": [], "vision_models": []})()

    for model in request.ocr_models or []:
        engine = get_ocr_module(model)
        res = engine.run(image)

        # Do not attempt fallbacks here; return the OCR engine result (including errors)
        # so callers see the actual engine runtime error if one occurs.
        ocr_results[model] = res

    for model in request.vision_models or []:
        engine = get_vision_module(model)
        vision_results[model] = engine.run(image)

    # Sanitize results to plain Python types (convert numpy types)
    return {
        "ocr_results": _sanitize_value(ocr_results),
        "vision_results": _sanitize_value(vision_results)
    }
