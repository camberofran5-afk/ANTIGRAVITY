"""
AI Data Parser - Gemini Integration

Parse unstructured data (text, images, voice) into structured records
"""

from typing import Dict, Any, Optional, List
import json
import re
from datetime import datetime
import structlog

logger = structlog.get_logger()


class DataParser:
    """Parse unstructured data using Gemini AI"""
    
    def __init__(self, ai_provider):
        """
        Initialize parser with AI provider
        
        Args:
            ai_provider: GeminiProvider instance
        """
        self.ai = ai_provider
    
    async def parse_cost_text(self, text: str) -> Dict[str, Any]:
        """
        Parse cost description into structured data
        
        Example:
            Input: "Compré 50 kg de alfalfa por $750 el 10 de enero"
            Output: {
                "category": "feed",
                "item": "alfalfa",
                "quantity": 50,
                "unit": "kg",
                "amount_mxn": 750,
                "date": "2026-01-10",
                "confidence": 0.95
            }
        """
        prompt = f"""
Analiza el siguiente texto sobre un gasto ganadero y extrae la información estructurada.

Texto: "{text}"

Extrae:
- category: categoría del gasto (feed, veterinary, labor, infrastructure, other)
- item: nombre del artículo o servicio
- quantity: cantidad (número)
- unit: unidad de medida
- amount_mxn: monto en pesos mexicanos
- date: fecha en formato YYYY-MM-DD (si dice "hoy" usa {datetime.now().strftime('%Y-%m-%d')})
- description: descripción breve

Responde SOLO con JSON válido, sin explicaciones adicionales.
"""
        
        try:
            response = await self.ai.generate_insight(
                prompt=prompt,
                context={"text": text},
                max_tokens=300
            )
            
            # Extract JSON from response
            result_text = response.get("insight", "{}")
            
            # Try to parse JSON
            try:
                # Find JSON in response
                json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
                if json_match:
                    parsed = json.loads(json_match.group())
                    parsed["confidence"] = response.get("confidence", 0.8)
                    parsed["raw_text"] = text
                    return parsed
            except json.JSONDecodeError:
                logger.warning("Failed to parse AI response as JSON", response=result_text)
            
            # Fallback: basic extraction
            return self._fallback_cost_extraction(text)
            
        except Exception as e:
            logger.error("Cost text parsing failed", error=str(e))
            return self._fallback_cost_extraction(text)
    
    def _fallback_cost_extraction(self, text: str) -> Dict[str, Any]:
        """Fallback extraction using regex"""
        result = {
            "description": text,
            "confidence": 0.3,
            "raw_text": text
        }
        
        # Extract amount
        amount_match = re.search(r'\$?\s*(\d+(?:,\d{3})*(?:\.\d{2})?)', text)
        if amount_match:
            amount_str = amount_match.group(1).replace(',', '')
            result["amount_mxn"] = float(amount_str)
        
        # Extract quantity
        qty_match = re.search(r'(\d+)\s*(kg|litros?|piezas?|unidades?)', text, re.IGNORECASE)
        if qty_match:
            result["quantity"] = int(qty_match.group(1))
            result["unit"] = qty_match.group(2).lower()
        
        # Detect category by keywords
        text_lower = text.lower()
        if any(word in text_lower for word in ['alimento', 'alfalfa', 'forraje', 'pasto']):
            result["category"] = "feed"
        elif any(word in text_lower for word in ['veterinario', 'vacuna', 'medicina']):
            result["category"] = "veterinary"
        elif any(word in text_lower for word in ['trabajador', 'salario', 'pago']):
            result["category"] = "labor"
        else:
            result["category"] = "other"
        
        return result
    
    async def parse_cattle_tag_image(self, image_data: bytes) -> Dict[str, Any]:
        """
        Parse cattle tag from image
        
        Example:
            Input: Photo of cattle tag "A-1234"
            Output: {
                "type": "cattle_tag",
                "arete_number": "A-1234",
                "confidence": 0.92
            }
        """
        # Note: This requires Gemini Vision API
        # For now, return placeholder
        logger.info("Image parsing not yet implemented")
        return {
            "type": "cattle_tag",
            "arete_number": None,
            "confidence": 0.0,
            "error": "Image parsing not yet implemented"
        }
    
    async def parse_voice_note(self, audio_data: bytes) -> Dict[str, Any]:
        """
        Parse voice note about cattle events
        
        Example:
            Input: "La vaca 234 tuvo un becerro hoy, peso 35 kilos"
            Output: {
                "type": "birth_event",
                "mother_id": "234",
                "calf_weight": 35,
                "date": "today",
                "confidence": 0.88
            }
        """
        # Note: This requires speech-to-text + Gemini
        # For now, return placeholder
        logger.info("Voice parsing not yet implemented")
        return {
            "type": "event",
            "confidence": 0.0,
            "error": "Voice parsing not yet implemented"
        }
    
    async def parse_event_text(self, text: str) -> Dict[str, Any]:
        """
        Parse event description into structured data
        
        Example:
            Input: "La vaca A-123 tuvo un becerro hoy"
            Output: {
                "type": "birth",
                "cattle_id": "A-123",
                "date": "2026-01-13",
                "notes": "becerro",
                "confidence": 0.90
            }
        """
        prompt = f"""
Analiza el siguiente texto sobre un evento ganadero y extrae la información estructurada.

Texto: "{text}"

Extrae:
- type: tipo de evento (birth, death, sale, vaccination, weighing, pregnancy_check, treatment)
- cattle_id: identificador del animal (número de arete)
- date: fecha en formato YYYY-MM-DD (si dice "hoy" usa {datetime.now().strftime('%Y-%m-%d')})
- data: datos adicionales relevantes (peso, vacuna, etc.)
- notes: notas adicionales

Responde SOLO con JSON válido, sin explicaciones adicionales.
"""
        
        try:
            response = await self.ai.generate_insight(
                prompt=prompt,
                context={"text": text},
                max_tokens=300
            )
            
            result_text = response.get("insight", "{}")
            
            # Try to parse JSON
            try:
                json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
                if json_match:
                    parsed = json.loads(json_match.group())
                    parsed["confidence"] = response.get("confidence", 0.8)
                    parsed["raw_text"] = text
                    return parsed
            except json.JSONDecodeError:
                logger.warning("Failed to parse AI response as JSON", response=result_text)
            
            return {"error": "Failed to parse", "raw_text": text, "confidence": 0.0}
            
        except Exception as e:
            logger.error("Event text parsing failed", error=str(e))
            return {"error": str(e), "raw_text": text, "confidence": 0.0}
