"""
Configuration settings for the PR automation application.
"""

import os
from typing import Optional

class Settings:
    """Application settings class."""
    
    def __init__(self):
        self.app_name = os.getenv("APP_NAME", "PR Automation Tool")
        self.debug = os.getenv("DEBUG", "false").lower() == "true"
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.api_timeout = int(os.getenv("API_TIMEOUT", "30"))
        self.max_retries = int(os.getenv("MAX_RETRIES", "3"))
        
    @property
    def database_url(self) -> Optional[str]:
        """Get database URL from environment."""
        return os.getenv("DATABASE_URL")
    
    @property
    def api_key(self) -> Optional[str]:
        """Get API key from environment."""
        return os.getenv("API_KEY")

settings = Settings()
