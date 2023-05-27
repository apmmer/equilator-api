from loguru import logger

from alembic import config as alembic_conf


def setup_db():
    logger.info("Setup test DB schema.")
    alembic_conf.main(argv=(["upgrade", "head"]))
    logger.info("DB setup performed.")

def teardown_db():
    logger.info("DB teardown process started")
    alembic_conf.main(argv=(["downgrade", "base"]))
    logger.info("DB downgraded")
