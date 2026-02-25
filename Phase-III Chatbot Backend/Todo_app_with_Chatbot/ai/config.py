"""AI chatbot configuration."""
import os
from dotenv import load_dotenv

load_dotenv()


class AIConfig:
    """AI chatbot configuration."""

    # Cohere API settings - NOT USED (using mock mode only)
    COHERE_API_KEY = os.getenv("COHERE_API_KEY")
    COHERE_MODEL = "mock-only"
    COHERE_BASE_URL = "https://api.cohere.com/v1"

    # ALWAYS use mock mode - no external API calls
    USE_MOCK = True

    # Temperature settings
    TEMPERATURE_TASK_OPERATIONS = 0.3  # Deterministic
    TEMPERATURE_CHAT = 0.5  # Conversational

    # Rate limiting
    RATE_LIMIT_PER_MINUTE = int(os.getenv("CHAT_RATE_LIMIT_PER_MINUTE", 60))
    RATE_LIMIT_PER_DAY = int(os.getenv("CHAT_RATE_LIMIT_PER_DAY", 1000))

    # Validation
    MAX_MESSAGE_LENGTH = 1000
    MAX_CONTENT_LENGTH = 10000

    @classmethod
    def validate(cls) -> bool:
        """Validate configuration."""
        return True

    @classmethod
    def get_temperature(cls, for_task: bool = True) -> float:
        """Get temperature setting based on operation type."""
        return cls.TEMPERATURE_TASK_OPERATIONS if for_task else cls.TEMPERATURE_CHAT


