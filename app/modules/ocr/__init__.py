from .tesseract import TesseractOCR
from .easyocr import EasyOCREngine

def get_ocr_module(name: str):
    if name == "tesseract":
        return TesseractOCR()
    if name == "easyocr":
        return EasyOCREngine()
    raise ValueError(f"OCR model not supported: {name}")

def list_ocr_models():
    return ["tesseract", "easyocr"]
