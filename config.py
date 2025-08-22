"""Configuration module for blackboard agents system."""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class that loads environment variables."""
    
    # LLM Provider Configuration
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "openai")
    
    # OpenAI Configuration
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    OPENAI_MAX_TOKENS: int = int(os.getenv("OPENAI_MAX_TOKENS", "500"))
    OPENAI_TEMPERATURE: float = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
    
    # Gemini Configuration
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    GEMINI_MAX_TOKENS: int = int(os.getenv("GEMINI_MAX_TOKENS", "500"))
    GEMINI_TEMPERATURE: float = float(os.getenv("GEMINI_TEMPERATURE", "0.7"))
    
    # System Configuration
    CONTEXT_WINDOW: int = int(os.getenv("CONTEXT_WINDOW", "5"))
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    DEBUG_DECISIONS: bool = os.getenv("DEBUG_DECISIONS", "false").lower() == "true"
    AGENT_WORD_LIMIT: int = int(os.getenv("AGENT_WORD_LIMIT", "100"))
    
    @classmethod
    def validate(cls) -> bool:
        """Validate that required configuration is present."""
        provider = cls.LLM_PROVIDER.lower()
        if provider == "openai" and not cls.OPENAI_API_KEY:
            return False
        elif provider == "gemini" and not cls.GEMINI_API_KEY:
            return False
        return True
    
    @classmethod
    def get_missing_vars(cls) -> list:
        """Get list of missing required environment variables."""
        missing = []
        provider = cls.LLM_PROVIDER.lower()
        if provider == "openai" and not cls.OPENAI_API_KEY:
            missing.append("OPENAI_API_KEY")
        elif provider == "gemini" and not cls.GEMINI_API_KEY:
            missing.append("GEMINI_API_KEY")
        return missing
