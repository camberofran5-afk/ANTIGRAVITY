"""
AI Response Caching Layer
Reduces API costs by caching responses for 24 hours
"""

from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import hashlib
import json
import structlog

logger = structlog.get_logger()


class AICache:
    """In-memory cache for AI responses"""
    
    def __init__(self, ttl_hours: int = 24):
        self.cache: Dict[str, tuple[Any, datetime]] = {}
        self.ttl = timedelta(hours=ttl_hours)
        self.hits = 0
        self.misses = 0
    
    def _generate_key(self, prompt: str, context: Dict[str, Any]) -> str:
        """Generate cache key from prompt and context"""
        # Create deterministic key from prompt + context
        data = {
            "prompt": prompt,
            "context": json.dumps(context, sort_keys=True)
        }
        key_string = json.dumps(data, sort_keys=True)
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def get(self, prompt: str, context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Get cached response if available and not expired"""
        key = self._generate_key(prompt, context)
        
        if key in self.cache:
            value, timestamp = self.cache[key]
            
            # Check if expired
            if datetime.now() - timestamp < self.ttl:
                self.hits += 1
                logger.info("ai_cache_hit", key=key[:8], age_hours=(datetime.now() - timestamp).total_seconds() / 3600)
                return value
            else:
                # Expired, remove
                del self.cache[key]
                logger.info("ai_cache_expired", key=key[:8])
        
        self.misses += 1
        return None
    
    def set(self, prompt: str, context: Dict[str, Any], value: Dict[str, Any]):
        """Cache a response"""
        key = self._generate_key(prompt, context)
        self.cache[key] = (value, datetime.now())
        logger.info("ai_cache_set", key=key[:8], cache_size=len(self.cache))
    
    def clear(self):
        """Clear all cached responses"""
        size = len(self.cache)
        self.cache.clear()
        logger.info("ai_cache_cleared", entries_removed=size)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        total_requests = self.hits + self.misses
        hit_rate = (self.hits / total_requests * 100) if total_requests > 0 else 0
        
        return {
            "hits": self.hits,
            "misses": self.misses,
            "total_requests": total_requests,
            "hit_rate_percent": round(hit_rate, 2),
            "cache_size": len(self.cache),
            "ttl_hours": self.ttl.total_seconds() / 3600
        }
    
    def cleanup_expired(self):
        """Remove expired entries"""
        now = datetime.now()
        expired_keys = [
            key for key, (_, timestamp) in self.cache.items()
            if now - timestamp >= self.ttl
        ]
        
        for key in expired_keys:
            del self.cache[key]
        
        if expired_keys:
            logger.info("ai_cache_cleanup", expired_count=len(expired_keys))


# Global cache instance
_cache = AICache(ttl_hours=24)


def get_cache() -> AICache:
    """Get global cache instance"""
    return _cache
