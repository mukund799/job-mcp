import os
from pydantic import BaseModel
class Config(BaseModel):
    """
    Configuration settings for the application.
    """
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    TIMEOUT: int = int(os.getenv("TIMEOUT", "30"))