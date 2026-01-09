"""
L1 Configuration: Ollama Configuration
Centralized configuration for Ollama local LLM hosting.
Following the 4-Layer Hierarchy: L1 = Configuration (Zero dependencies on other layers)
"""

import os
from enum import Enum
from typing import TypedDict, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class OllamaModel(str, Enum):
    """Available Ollama models for different tasks."""
    # Language models
    LLAMA3_8B = "llama3"
    LLAMA3_70B = "llama3:70b"
    MISTRAL_7B = "mistral"
    MISTRAL_NEMO = "mistral-nemo"
    QWQ_32B = "qwq"  # Reasoning-focused model
    GEMMA_7B = "gemma:7b"
    
    # Vision models
    LLAVA = "llava"
    MINICPM_V = "minicpm-v"
    
    # Embedding models
    NOMIC_EMBED = "nomic-embed-text"
    MXBAI_EMBED = "mxbai-embed-large"


class OllamaConfig(TypedDict):
    """Ollama configuration structure."""
    base_url: str
    timeout: int
    default_model: str
    temperature: float
    max_tokens: int


class OllamaSettings:
    """
    Centralized Ollama configuration.
    
    Provides configuration for local LLM hosting via Ollama.
    Supports text generation, vision, and embeddings.
    """
    
    # Default Ollama endpoint
    DEFAULT_BASE_URL = "http://localhost:11434"
    
    # OpenAI-compatible endpoint (for drop-in replacement)
    OPENAI_COMPATIBLE_URL = "http://localhost:11434/v1"
    
    # Default model settings
    DEFAULT_MODEL = OllamaModel.LLAMA3_8B
    DEFAULT_VISION_MODEL = OllamaModel.LLAVA
    DEFAULT_EMBEDDING_MODEL = OllamaModel.NOMIC_EMBED
    
    # Generation parameters
    DEFAULT_TEMPERATURE = 0.7
    DEFAULT_MAX_TOKENS = 4096
    DEFAULT_TIMEOUT = 120  # seconds
    
    # Streaming settings
    ENABLE_STREAMING = True
    
    # Model-specific configurations
    MODEL_CONFIGS = {
        OllamaModel.LLAMA3_8B: {
            "context_window": 8192,
            "best_for": "General purpose, fast responses",
            "requires_gpu": False,
        },
        OllamaModel.LLAMA3_70B: {
            "context_window": 8192,
            "best_for": "Complex reasoning, high quality",
            "requires_gpu": True,
        },
        OllamaModel.MISTRAL_7B: {
            "context_window": 8192,
            "best_for": "Balanced performance and speed",
            "requires_gpu": False,
        },
        OllamaModel.QWQ_32B: {
            "context_window": 32768,
            "best_for": "Long context, reasoning tasks",
            "requires_gpu": True,
        },
        OllamaModel.LLAVA: {
            "context_window": 4096,
            "best_for": "Image understanding",
            "requires_gpu": True,
        },
        OllamaModel.MINICPM_V: {
            "context_window": 4096,
            "best_for": "Vision + language tasks",
            "requires_gpu": True,
        },
    }
    
    def __init__(self):
        """Initialize Ollama configuration from environment variables."""
        self.base_url: str = os.getenv(
            "OLLAMA_BASE_URL", 
            self.DEFAULT_BASE_URL
        )
        self.openai_compatible_url: str = os.getenv(
            "OLLAMA_OPENAI_URL",
            self.OPENAI_COMPATIBLE_URL
        )
        self.default_model: str = os.getenv(
            "OLLAMA_DEFAULT_MODEL",
            self.DEFAULT_MODEL.value
        )
        self.temperature: float = float(os.getenv(
            "OLLAMA_TEMPERATURE",
            str(self.DEFAULT_TEMPERATURE)
        ))
        self.max_tokens: int = int(os.getenv(
            "OLLAMA_MAX_TOKENS",
            str(self.DEFAULT_MAX_TOKENS)
        ))
        self.timeout: int = int(os.getenv(
            "OLLAMA_TIMEOUT",
            str(self.DEFAULT_TIMEOUT)
        ))
        self.enable_streaming: bool = os.getenv(
            "OLLAMA_STREAMING",
            "true"
        ).lower() == "true"
    
    def get_config(self) -> OllamaConfig:
        """
        Get Ollama configuration as a dictionary.
        
        Returns:
            OllamaConfig dictionary with all settings
        """
        return {
            "base_url": self.base_url,
            "timeout": self.timeout,
            "default_model": self.default_model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
    
    def get_model_info(self, model: OllamaModel) -> dict:
        """
        Get information about a specific model.
        
        Args:
            model: The Ollama model to get info for
            
        Returns:
            Dictionary with model information
        """
        return self.MODEL_CONFIGS.get(model, {})
    
    def is_available(self) -> bool:
        """
        Check if Ollama is available at the configured endpoint.
        
        Returns:
            True if Ollama is reachable, False otherwise
        """
        try:
            import requests
            response = requests.get(
                f"{self.base_url}/api/tags",
                timeout=5
            )
            return response.status_code == 200
        except Exception:
            return False


# Singleton instance
_ollama_settings: Optional[OllamaSettings] = None


def get_ollama_settings() -> OllamaSettings:
    """
    Get the singleton Ollama settings instance.
    
    Returns:
        OllamaSettings instance
        
    Example:
        >>> from tools.L1_config.ollama_config import get_ollama_settings
        >>> settings = get_ollama_settings()
        >>> print(settings.base_url)
        http://localhost:11434
    """
    global _ollama_settings
    
    if _ollama_settings is None:
        _ollama_settings = OllamaSettings()
    
    return _ollama_settings


if __name__ == "__main__":
    # Test the configuration
    print("🔍 Testing Ollama Configuration...")
    print()
    
    settings = get_ollama_settings()
    
    print("✅ Ollama Configuration loaded")
    print()
    print(f"Base URL: {settings.base_url}")
    print(f"OpenAI Compatible URL: {settings.openai_compatible_url}")
    print(f"Default Model: {settings.default_model}")
    print(f"Temperature: {settings.temperature}")
    print(f"Max Tokens: {settings.max_tokens}")
    print(f"Timeout: {settings.timeout}s")
    print(f"Streaming: {settings.enable_streaming}")
    print()
    
    # Check availability
    print("🔌 Checking Ollama availability...")
    if settings.is_available():
        print("✅ Ollama is running and accessible")
    else:
        print("⚠️  Ollama is not running or not accessible")
        print(f"   Make sure Ollama is installed and running at {settings.base_url}")
    print()
    
    # Show available models
    print("📋 Available Models:")
    for model in OllamaModel:
        info = settings.get_model_info(model)
        if info:
            print(f"  • {model.value}")
            print(f"    Best for: {info.get('best_for', 'N/A')}")
            print(f"    Context: {info.get('context_window', 'N/A')} tokens")
            print(f"    GPU: {'Required' if info.get('requires_gpu') else 'Optional'}")
