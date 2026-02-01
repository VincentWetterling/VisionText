from .base import OCRBase

class EasyOCREngine(OCRBase):
    def __init__(self):
        # lazy import to avoid heavy startup when not used
        try:
            import easyocr
            self.reader = easyocr.Reader(['en'])
        except Exception:
            self.reader = None

    def run(self, image):
        if self.reader is None:
            return {"error": "easyocr not available"}
        # EasyOCR accepts: file path (str), bytes, or numpy array.
        # Convert PIL Image to numpy array here to ensure compatibility.
        try:
            # locally import to keep module lightweight until used
            from PIL import Image as PILImage
            import numpy as np
        except Exception:
            PILImage = None
            np = None

        img_input = image
        # If it's a PIL Image, convert to RGB numpy array
        if PILImage is not None and isinstance(image, PILImage.Image):
            img_input = np.array(image.convert("RGB"))

        try:
            res = self.reader.readtext(img_input)
            return res
        except Exception as e:
            return {"error": f"easyocr failed: {e}"}
