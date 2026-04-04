from pathlib import Path
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    APP_NAME: str = "Medical Segmentation API"
    API_V1_STR: str = "/api/v1"
    
    BASE_DIR: Path = Path(__file__).parent.parent.parent.parent 
    DATA_DIR: Path = BASE_DIR / "data" / "external"              
    DICOM_DIR: Path = DATA_DIR / "dicoms"
    RESULTS_DIR: Path = DATA_DIR / "results"
    DB_PATH: Path = DATA_DIR / "studies.db"
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()