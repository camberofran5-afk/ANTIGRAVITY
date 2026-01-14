"""
ERP Ganadero - KPI Calculator (L3 Business Logic)

Calculate key performance indicators for cattle operations.
"""

from typing import Dict, Any
from datetime import datetime, timedelta
from ..L2_foundation.cattle_crud import get_cattle_crud
from ..L2_foundation.event_crud import get_event_crud
from ..L1_config.cattle_types import EventType, Status, HerdMetrics
from ..L1_config.system_config import KPI_TARGETS
import structlog

logger = structlog.get_logger()


class KPICalculator:
    """Calculate herd KPIs"""
    
    def __init__(self):
        self.cattle_crud = get_cattle_crud()
        self.event_crud = get_event_crud()
    
    async def calculate_herd_metrics(self, ranch_id: str) -> HerdMetrics:
        """Calculate all KPIs for a ranch"""
        
        # Get all active cattle
        cattle = await self.cattle_crud.list_by_ranch(
            ranch_id, 
            status=Status.ACTIVE,
            limit=1000
        )
        
        # Calculate each metric
        pregnancy_rate = await self._calculate_pregnancy_rate(ranch_id, cattle)
        calving_interval = await self._calculate_calving_interval(ranch_id)
        weaning_weight = await self._calculate_weaning_weight(ranch_id)
        calf_mortality = await self._calculate_calf_mortality(ranch_id)
        
        return HerdMetrics(
            pregnancy_rate=pregnancy_rate,
            calving_interval_days=calving_interval,
            weaning_weight_avg=weaning_weight,
            calf_mortality_percent=calf_mortality,
            calculated_at=datetime.utcnow(),
            source="fresh"
        )
    
    async def _calculate_pregnancy_rate(self, ranch_id: str, cattle: list) -> float:
        """Calculate pregnancy rate (% of cows pregnant)"""
        # Simplified: count pregnancy_check events in last 6 months
        # Real implementation would track actual pregnancy status
        
        total_cows = len([c for c in cattle if c.species.value == "vaca"])
        if total_cows == 0:
            return 0.0
        
        # Mock calculation - in production, query pregnancy_check events
        # and count positive results
        pregnant_count = int(total_cows * 0.78)  # Using research data
        
        return (pregnant_count / total_cows) * 100
    
    async def _calculate_calving_interval(self, ranch_id: str) -> float:
        """Calculate average calving interval (days between births)"""
        # Simplified: average time between birth events per cow
        # Real implementation would track per-cow intervals
        
        # Mock calculation based on research
        return 412.0  # From research data
    
    async def _calculate_weaning_weight(self, ranch_id: str) -> float:
        """Calculate average weaning weight"""
        # Query weighing events for calves at ~6-8 months
        # Real implementation would filter by age at weighing
        
        # Mock calculation
        return 185.0  # From research data
    
    async def _calculate_calf_mortality(self, ranch_id: str) -> float:
        """Calculate calf mortality rate"""
        # Count death events for calves vs total births
        # Real implementation would track births and deaths
        
        # Mock calculation
        return 4.2  # From research data
    
    def get_metric_status(self, metric_name: str, value: float) -> str:
        """Determine if metric is optimal, warning, or critical"""
        target = KPI_TARGETS.get(metric_name)
        if not target:
            return "optimal"
        
        # Define thresholds
        if metric_name == "pregnancy_rate":
            if value >= target:
                return "optimal"
            elif value >= target * 0.9:
                return "warning"
            else:
                return "critical"
        
        elif metric_name == "calving_interval_days":
            if value <= target:
                return "optimal"
            elif value <= target * 1.1:
                return "warning"
            else:
                return "critical"
        
        elif metric_name == "weaning_weight_kg":
            if value >= target:
                return "optimal"
            elif value >= target * 0.9:
                return "warning"
            else:
                return "critical"
        
        elif metric_name == "calf_mortality_percent":
            if value <= target:
                return "optimal"
            elif value <= target * 1.5:
                return "warning"
            else:
                return "critical"
        
        return "optimal"


def get_kpi_calculator() -> KPICalculator:
    """Get KPI calculator instance"""
    return KPICalculator()
