import pytesseract
from .base import OCRBase

class TesseractOCR(OCRBase):
    def run(self, image):
        return pytesseract.image_to_string(image)
