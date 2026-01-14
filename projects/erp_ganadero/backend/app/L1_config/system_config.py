"""
ERP Ganadero - System Configuration (L1)

Application constants and settings.
"""

from typing import Dict, Any


# Application Settings
APP_NAME = "ERP Ganadero"
APP_VERSION = "1.0.0"
API_PREFIX = "/api/v1"

# Pagination
DEFAULT_PAGE_SIZE = 50
MAX_PAGE_SIZE = 100

# File Upload
MAX_PHOTO_SIZE_MB = 5
ALLOWED_PHOTO_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
PHOTO_COMPRESSION_QUALITY = 85
PHOTO_MAX_DIMENSION = 1920

# Sync
SYNC_BATCH_SIZE = 100
SYNC_RETRY_LIMIT = 3

# KPI Targets (Industry Benchmarks)
KPI_TARGETS: Dict[str, Any] = {
    "pregnancy_rate": 85.0,  # %
    "calving_interval_days": 365,  # days
    "weaning_weight_kg": 210,  # kg
    "calf_mortality_percent": 3.0,  # %
}

# Cost Estimates (USD per day)
COST_PER_COW_PER_DAY_USD = 2.50

# Unproductive Cow Criteria
UNPRODUCTIVE_MONTHS_THRESHOLD = 18  # months since last calf

# CORS Settings
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:19006",  # Expo
    "exp://localhost:19000",  # Expo
]

# Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "json"
