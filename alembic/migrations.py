"""
Script for migrations
"""

from loguru import logger

from alembic import config

logger.info("Started migrations.")
config.main(argv=(["upgrade", "head"]))
logger.info("Migrations performed successfully")
