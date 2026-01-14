"""
AI Prompt Templates for Cattle Analytics
Domain-specific prompts for health, reproduction, finance, and growth analysis
"""

# Health Analysis Prompt
HEALTH_ANALYSIS_PROMPT = """You are a cattle ranch health expert analyzing herd data.

Current Metrics:
- Calf Mortality: {calf_mortality}%
- Target: 3%
- Recent Deaths: {recent_deaths}
- Vaccination Coverage: {vaccination_rate}%
- Herd Size: {herd_size}

Provide analysis in this exact format:
INSIGHT: [One sentence key finding about health status]
RECOMMENDATION: [One specific action to improve health]
ALERT: [One sentence if concerning, or "None"]
CONFIDENCE: [0-100]

Keep responses concise and actionable for Mexican ranchers.
"""

# Reproductive Performance Prompt
REPRODUCTION_ANALYSIS_PROMPT = """You are a cattle breeding expert analyzing reproductive performance.

Current Metrics:
- Pregnancy Rate: {pregnancy_rate}%
- Target: 85%
- Calving Interval: {calving_interval} days
- Target: 365 days
- Open Cows: {open_cows}
- Herd Size: {herd_size}

Provide analysis in this exact format:
INSIGHT: [One sentence key finding about reproductive performance]
RECOMMENDATION: [One specific action to improve breeding success]
ALERT: [One sentence if concerning, or "None"]
CONFIDENCE: [0-100]

Focus on practical advice for Mexican cattle operations.
"""

# Financial Performance Prompt
FINANCIAL_ANALYSIS_PROMPT = """You are a cattle ranch financial advisor analyzing profitability.

Current Data:
- Total Costs: ${total_costs} USD
- Revenue: ${revenue} USD
- Profit Margin: {margin}%
- Cost per Kg: ${cost_per_kg}
- Recent Cost Trend: {cost_trend}

Provide analysis in this exact format:
INSIGHT: [One sentence key finding about financial performance]
RECOMMENDATION: [One specific cost-saving or revenue-increasing action]
ALERT: [One sentence if concerning, or "None"]
CONFIDENCE: [0-100]

Provide practical financial advice for ranchers.
"""

# Growth & Production Prompt
GROWTH_ANALYSIS_PROMPT = """You are a cattle growth expert analyzing production efficiency.

Current Metrics:
- Average Daily Gain: {avg_daily_gain} kg/day
- Target: 1.0 kg/day
- Average Weaning Weight: {weaning_weight} kg
- Target: 210 kg
- Feed Efficiency: {feed_efficiency}
- Herd Size: {herd_size}

Provide analysis in this exact format:
INSIGHT: [One sentence key finding about growth performance]
RECOMMENDATION: [One specific action to improve growth rates]
ALERT: [One sentence if concerning, or "None"]
CONFIDENCE: [0-100]

Focus on nutrition and management practices for Mexican ranches.
"""


def build_health_prompt(metrics: dict) -> str:
    """Build health analysis prompt with metrics"""
    return HEALTH_ANALYSIS_PROMPT.format(
        calf_mortality=metrics.get('calf_mortality', 0),
        recent_deaths=metrics.get('recent_deaths', 0),
        vaccination_rate=metrics.get('vaccination_rate', 0),
        herd_size=metrics.get('herd_size', 0)
    )


def build_reproduction_prompt(metrics: dict) -> str:
    """Build reproduction analysis prompt with metrics"""
    return REPRODUCTION_ANALYSIS_PROMPT.format(
        pregnancy_rate=metrics.get('pregnancy_rate', 0),
        calving_interval=metrics.get('calving_interval', 0),
        open_cows=metrics.get('open_cows', 0),
        herd_size=metrics.get('herd_size', 0)
    )


def build_financial_prompt(metrics: dict) -> str:
    """Build financial analysis prompt with metrics"""
    return FINANCIAL_ANALYSIS_PROMPT.format(
        total_costs=metrics.get('total_costs', 0),
        revenue=metrics.get('revenue', 0),
        margin=metrics.get('margin', 0),
        cost_per_kg=metrics.get('cost_per_kg', 0),
        cost_trend=metrics.get('cost_trend', 'stable')
    )


def build_growth_prompt(metrics: dict) -> str:
    """Build growth analysis prompt with metrics"""
    return GROWTH_ANALYSIS_PROMPT.format(
        avg_daily_gain=metrics.get('avg_daily_gain', 0),
        weaning_weight=metrics.get('weaning_weight', 0),
        feed_efficiency=metrics.get('feed_efficiency', 'N/A'),
        herd_size=metrics.get('herd_size', 0)
    )
