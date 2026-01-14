"""
Initialize database and create tables on startup.
"""

from app.L1_config.database import init_db, engine
from app.L1_config.models import Base
import structlog

logger = structlog.get_logger()


def initialize_database():
    """Create all database tables"""
    try:
        logger.info("Initializing database...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error("Database initialization failed", error=str(e))
        raise


if __name__ == "__main__":
    initialize_database()
