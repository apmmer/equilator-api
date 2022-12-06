import logging

from alembic import config

logging.info("Setup test DB schema.")
config.main(argv=(["upgrade", "head"]))
logging.info("DB schema success setup finished")
