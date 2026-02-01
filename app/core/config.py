from pathlib import Path
from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "VisionText"
    model_cache_dir: Path = Path("./models")

settings = Settings()
