from pathlib import Path
from pydantic import BaseSettings

class Settings(BaseSettings):
    model_path: Path = Path("models/ggml-model.bin")
    n_ctx: int = 2048
    n_threads: int = 4
    log_level: str = "INFO"

settings = Settings()
