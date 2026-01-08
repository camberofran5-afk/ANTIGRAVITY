"""
L1 Configuration: LLM Client Initialization
Provides centralized LLM clients for Gemini and Perplexity.
Following the 4-Layer Hierarchy: L1 = Configuration (Zero dependencies on other layers)
"""

import os
from typing import Optional
from dotenv import load_dotenv
import google.generativeai as genai
from openai import OpenAI

# Load environment variables
load_dotenv()


class LLMConfig:
    """
    Centralized LLM configuration for all AI providers.
    
    Supports:
    - Google Gemini (via google-generativeai)
    - Perplexity (via OpenAI-compatible API)
    - OpenAI (optional)
    - Anthropic (optional)
    """
    
    def __init__(self):
        """Initialize LLM configuration from environment variables."""
        self.gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
        self.perplexity_api_key: str = os.getenv("PERPLEXITY_API_KEY", "")
        self.openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
        self.anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
        
        # Configure Gemini if key is available
        if self.gemini_api_key and self.gemini_api_key != "[key]":
            genai.configure(api_key=self.gemini_api_key)
    
    def get_gemini_model(self, model_name: str = "gemini-pro") -> genai.GenerativeModel:
        """
        Get a Gemini model instance.
        
        Args:
            model_name: Name of the Gemini model (default: "gemini-pro")
                       Options: "gemini-pro", "gemini-pro-vision"
        
        Returns:
            Gemini GenerativeModel instance
            
        Raises:
            ValueError: If Gemini API key is not configured
            
        Example:
            >>> model = get_gemini_model()
            >>> response = model.generate_content("Hello, world!")
        """
        if not self.gemini_api_key or self.gemini_api_key == "[key]":
            raise ValueError(
                "Gemini API key not configured. "
                "Set GEMINI_API_KEY in .env"
            )
        
        return genai.GenerativeModel(model_name)
    
    def get_perplexity_client(self) -> OpenAI:
        """
        Get a Perplexity client instance.
        
        Perplexity uses an OpenAI-compatible API.
        
        Returns:
            OpenAI client configured for Perplexity
            
        Raises:
            ValueError: If Perplexity API key is not configured
            
        Example:
            >>> client = get_perplexity_client()
            >>> response = client.chat.completions.create(
            ...     model="llama-3.1-sonar-small-128k-online",
            ...     messages=[{"role": "user", "content": "Hello"}]
            ... )
        """
        if not self.perplexity_api_key or self.perplexity_api_key == "[key]":
            raise ValueError(
                "Perplexity API key not configured. "
                "Set PERPLEXITY_API_KEY in .env"
            )
        
        return OpenAI(
            api_key=self.perplexity_api_key,
            base_url="https://api.perplexity.ai"
        )
    
    def get_openai_client(self) -> OpenAI:
        """
        Get an OpenAI client instance.
        
        Returns:
            OpenAI client instance
            
        Raises:
            ValueError: If OpenAI API key is not configured
        """
        if not self.openai_api_key or self.openai_api_key == "[key]":
            raise ValueError(
                "OpenAI API key not configured. "
                "Set OPENAI_API_KEY in .env"
            )
        
        return OpenAI(api_key=self.openai_api_key)


# Singleton instance
_llm_config: Optional[LLMConfig] = None


def get_gemini_model(model_name: str = "gemini-1.5-flash") -> genai.GenerativeModel:
    """
    Get a Gemini model instance.
    
    This is the primary way to access Gemini throughout the application.
    
    Args:
        model_name: Name of the Gemini model (default: "gemini-1.5-flash")
                   Options: "gemini-1.5-flash", "gemini-1.5-pro"
    
    Returns:
        Gemini GenerativeModel instance
        
    Example:
        >>> from tools.L1_config.llm_client import get_gemini_model
        >>> model = get_gemini_model()
        >>> response = model.generate_content("Explain quantum computing")
        >>> print(response.text)
    """
    global _llm_config
    
    if _llm_config is None:
        _llm_config = LLMConfig()
    
    return _llm_config.get_gemini_model(model_name)


def get_perplexity_client() -> OpenAI:
    """
    Get a Perplexity client instance.
    
    This is the primary way to access Perplexity throughout the application.
    
    Returns:
        OpenAI client configured for Perplexity
        
    Example:
        >>> from tools.L1_config.llm_client import get_perplexity_client
        >>> client = get_perplexity_client()
        >>> response = client.chat.completions.create(
        ...     model="llama-3.1-sonar-small-128k-online",
        ...     messages=[{"role": "user", "content": "Latest AI news"}]
        ... )
        >>> print(response.choices[0].message.content)
    """
    global _llm_config
    
    if _llm_config is None:
        _llm_config = LLMConfig()
    
    return _llm_config.get_perplexity_client()


def get_openai_client() -> OpenAI:
    """Get an OpenAI client instance."""
    global _llm_config
    
    if _llm_config is None:
        _llm_config = LLMConfig()
    
    return _llm_config.get_openai_client()


if __name__ == "__main__":
    # Test the configuration
    print("🔍 Testing LLM Configuration...")
    print()
    
    try:
        config = LLMConfig()
        print("✅ LLM Configuration loaded successfully")
        print()
        
        # Test Gemini
        if config.gemini_api_key and config.gemini_api_key != "[key]":
            print("✅ Gemini API Key: Configured")
            print(f"   Key: {config.gemini_api_key[:20]}... ({len(config.gemini_api_key)} chars)")
            model = get_gemini_model()
            print(f"   Model type: {type(model).__name__}")
        else:
            print("⚠️  Gemini API Key: Not configured")
        print()
        
        # Test Perplexity
        if config.perplexity_api_key and config.perplexity_api_key != "[key]":
            print("✅ Perplexity API Key: Configured")
            print(f"   Key: {config.perplexity_api_key[:20]}... ({len(config.perplexity_api_key)} chars)")
            client = get_perplexity_client()
            print(f"   Client type: {type(client).__name__}")
        else:
            print("⚠️  Perplexity API Key: Not configured")
        print()
        
        print("🎯 LLM clients ready to use!")
        print()
        print("Usage:")
        print("  # Gemini")
        print("  from tools.L1_config.llm_client import get_gemini_model")
        print("  model = get_gemini_model()")
        print("  response = model.generate_content('Your prompt')")
        print()
        print("  # Perplexity")
        print("  from tools.L1_config.llm_client import get_perplexity_client")
        print("  client = get_perplexity_client()")
        print("  response = client.chat.completions.create(...)")
        
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        exit(1)
