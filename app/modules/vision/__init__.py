from .blip import BLIPVision

def get_vision_module(name: str):
    if name == "blip":
        return BLIPVision()
    raise ValueError(f"Vision model not supported: {name}")

def list_vision_models():
    return ["blip"]
