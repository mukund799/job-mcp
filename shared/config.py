import os
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
class Config(BaseModel):
    """
    Configuration settings for the application.
    """
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    TIMEOUT: int = int(os.getenv("TIMEOUT", "30"))
    GMAIL_ADDRESS: str = os.getenv("GMAIL_ADDRESS", "")
    GMAIL_APP_PASSWORD: str = os.getenv("GMAIL_APP_PASSWORD", "")