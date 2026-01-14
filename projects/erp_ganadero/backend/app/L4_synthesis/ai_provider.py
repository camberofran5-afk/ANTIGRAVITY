"""
AI Provider Abstraction Layer for ERP Ganadero
Supports multiple LLM providers with unified interface
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
import os
from datetime import datetime
import structlog

logger = structlog.get_logger()


class AIProvider(ABC):
    """Abstract base class for AI providers"""
    
    @abstractmethod
    async def generate_insight(
        self, 
        prompt: str, 
        context: Dict[str, Any],
        max_tokens: int = 500
    ) -> Dict[str, Any]:
        """
        Generate AI insight from prompt and context
        
        Returns:
            {
                "insight": str,
                "recommendation": str,
                "alert": str,
                "confidence": int (0-100)
            }
        """
        pass
    
    @abstractmethod
    def get_cost_estimate(self, prompt_tokens: int, response_tokens: int) -> float:
        """Estimate cost in USD for a request"""
        pass


class GeminiProvider(AIProvider):
    """Google Gemini Pro provider"""
    
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            logger.warning("GOOGLE_API_KEY not found - AI analytics will not work")
            self.api_key = "dummy-key-for-development"  # Allow server to start
        
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            # Try new API first, fall back to old API
            try:
                self.model = genai.GenerativeModel('gemini-pro')
            except (AttributeError, Exception):
                # Older API or different structure
                logger.warning("Could not initialize Gemini model - using fallback")
                self.model = None
            self.genai = genai
            self.available = True if self.model else False
        except ImportError:
            logger.warning("google-generativeai package not installed - AI features disabled")
            self.model = None
            self.genai = None
            self.available = False
    
    async def generate_insight(
        self, 
        prompt: str, 
        context: Dict[str, Any],
        max_tokens: int = 500
    ) -> Dict[str, Any]:
        """Generate insight using Gemini Pro"""
        if not self.available:
            return {
                "insight": "AI service not available",
                "recommendation": "Install google-generativeai package",
                "alert": None,
                "confidence": 0,
                "provider": "gemini-pro (unavailable)",
                "generated_at": datetime.now().isoformat()
            }
        
        try:
            # Generate content
            response = self.model.generate_content(prompt)
            
            # Parse structured response
            text = response.text
            insight = self._extract_field(text, "INSIGHT")
            recommendation = self._extract_field(text, "RECOMMENDATION")
            alert = self._extract_field(text, "ALERT")
            confidence = self._extract_confidence(text)
            
            logger.info("gemini_insight_generated", 
                       confidence=confidence,
                       has_alert=alert != "None")
            
            return {
                "insight": insight,
                "recommendation": recommendation,
                "alert": alert if alert != "None" else None,
                "confidence": confidence,
                "provider": "gemini-pro",
                "generated_at": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error("gemini_generation_failed", error=str(e))
            raise
    
    def _extract_field(self, text: str, field: str) -> str:
        """Extract field from formatted response"""
        try:
            marker = f"{field}:"
            if marker in text:
                start = text.index(marker) + len(marker)
                # Find next field or end
                end = len(text)
                for next_field in ["INSIGHT:", "RECOMMENDATION:", "ALERT:", "CONFIDENCE:"]:
                    if next_field in text[start:]:
                        end = start + text[start:].index(next_field)
                        break
                return text[start:end].strip()
            return "N/A"
        except Exception:
            return "N/A"
    
    def _extract_confidence(self, text: str) -> int:
        """Extract confidence score"""
        try:
            if "CONFIDENCE:" in text:
                conf_text = self._extract_field(text, "CONFIDENCE")
                # Extract number
                import re
                match = re.search(r'\d+', conf_text)
                if match:
                    return min(100, max(0, int(match.group())))
            return 75  # Default confidence
        except Exception:
            return 75
    
    def get_cost_estimate(self, prompt_tokens: int, response_tokens: int) -> float:
        """Estimate cost for Gemini Pro"""
        # Gemini Pro pricing: $0.50 per 1M input, $1.50 per 1M output
        input_cost = (prompt_tokens / 1_000_000) * 0.50
        output_cost = (response_tokens / 1_000_000) * 1.50
        return input_cost + output_cost


class OpenAIProvider(AIProvider):
    """OpenAI GPT-4 provider (fallback)"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found")
        
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=self.api_key)
        except ImportError:
            raise ImportError("openai package not installed")
    
    async def generate_insight(
        self, 
        prompt: str, 
        context: Dict[str, Any],
        max_tokens: int = 500
    ) -> Dict[str, Any]:
        """Generate insight using GPT-4"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a cattle ranch management expert."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens
            )
            
            text = response.choices[0].message.content
            
            # Parse structured response (same as Gemini)
            gemini_parser = GeminiProvider.__new__(GeminiProvider)
            insight = gemini_parser._extract_field(text, "INSIGHT")
            recommendation = gemini_parser._extract_field(text, "RECOMMENDATION")
            alert = gemini_parser._extract_field(text, "ALERT")
            confidence = gemini_parser._extract_confidence(text)
            
            return {
                "insight": insight,
                "recommendation": recommendation,
                "alert": alert if alert != "None" else None,
                "confidence": confidence,
                "provider": "gpt-4",
                "generated_at": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error("openai_generation_failed", error=str(e))
            raise
    
    def get_cost_estimate(self, prompt_tokens: int, response_tokens: int) -> float:
        """Estimate cost for GPT-4"""
        # GPT-4 pricing: $30 per 1M input, $60 per 1M output
        input_cost = (prompt_tokens / 1_000_000) * 30.00
        output_cost = (response_tokens / 1_000_000) * 60.00
        return input_cost + output_cost


def get_ai_provider(provider_name: str = "gemini") -> AIProvider:
    """Factory function to get AI provider"""
    providers = {
        "gemini": GeminiProvider,
        "openai": OpenAIProvider
    }
    
    if provider_name not in providers:
        raise ValueError(f"Unknown provider: {provider_name}")
    
    return providers[provider_name]()
