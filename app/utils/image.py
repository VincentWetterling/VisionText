from io import BytesIO
from PIL import Image

def load_image(image_bytes):
    return Image.open(BytesIO(image_bytes)).convert("RGB")
