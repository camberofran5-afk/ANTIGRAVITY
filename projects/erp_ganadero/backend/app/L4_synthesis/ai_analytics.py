"""
AI Analytics Service
Generates insights for health, reproduction, finance, and growth
"""

from typing import Dict, Any
from app.L4_synthesis.ai_provider import get_ai_provider, AIProvider
from app.L4_synthesis.ai_cache import get_cache
from app.L1_config.ai_prompts import (
    build_health_prompt,
    build_reproduction_prompt,
    build_financial_prompt,
    build_growth_prompt
)
import structlog

logger = structlog.get_logger()


class AIAnalyticsService:
    """Service for generating AI-powered analytics insights"""
    
    def __init__(self, provider_name: str = "gemini"):
        self.provider: AIProvider = get_ai_provider(provider_name)
        self.cache = get_cache()
    
    async def analyze_health(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Generate health insights"""
        prompt = build_health_prompt(metrics)
        context = {"type": "health", "metrics": metrics}
        
        # Check cache first
        cached = self.cache.get(prompt, context)
        if cached:
            return cached
        
        # Generate new insight
        try:
            result = await self.provider.generate_insight(prompt, context)
            self.cache.set(prompt, context, result)
            
            logger.info("health_insight_generated", 
                       confidence=result.get('confidence'),
                       cached=False)
            
            return result
        except Exception as e:
            logger.error("health_analysis_failed", error=str(e))
            return self._fallback_response("health")
    
    async def analyze_reproduction(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Generate reproductive performance insights"""
        prompt = build_reproduction_prompt(metrics)
        context = {"type": "reproduction", "metrics": metrics}
        
        # Check cache
        cached = self.cache.get(prompt, context)
        if cached:
            return cached
        
        # Generate new insight
        try:
            result = await self.provider.generate_insight(prompt, context)
            self.cache.set(prompt, context, result)
            
            logger.info("reproduction_insight_generated",
                       confidence=result.get('confidence'),
                       cached=False)
            
            return result
        except Exception as e:
            logger.error("reproduction_analysis_failed", error=str(e))
            return self._fallback_response("reproduction")
    
    async def analyze_financial(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Generate financial insights"""
        prompt = build_financial_prompt(metrics)
        context = {"type": "financial", "metrics": metrics}
        
        # Check cache
        cached = self.cache.get(prompt, context)
        if cached:
            return cached
        
        # Generate new insight
        try:
            result = await self.provider.generate_insight(prompt, context)
            self.cache.set(prompt, context, result)
            
            logger.info("financial_insight_generated",
                       confidence=result.get('confidence'),
                       cached=False)
            
            return result
        except Exception as e:
            logger.error("financial_analysis_failed", error=str(e))
            return self._fallback_response("financial")
    
    async def analyze_growth(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Generate growth & production insights"""
        prompt = build_growth_prompt(metrics)
        context = {"type": "growth", "metrics": metrics}
        
        # Check cache
        cached = self.cache.get(prompt, context)
        if cached:
            return cached
        
        # Generate new insight
        try:
            result = await self.provider.generate_insight(prompt, context)
            self.cache.set(prompt, context, result)
            
            logger.info("growth_insight_generated",
                       confidence=result.get('confidence'),
                       cached=False)
            
            return result
        except Exception as e:
            logger.error("growth_analysis_failed", error=str(e))
            return self._fallback_response("growth")
    
    def _fallback_response(self, analysis_type: str) -> Dict[str, Any]:
        """Fallback response when AI fails"""
        return {
            "insight": f"Unable to generate {analysis_type} insights at this time.",
            "recommendation": "Please check your data and try again later.",
            "alert": None,
            "confidence": 0,
            "provider": "fallback",
            "error": True
        }
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        return self.cache.get_stats()
