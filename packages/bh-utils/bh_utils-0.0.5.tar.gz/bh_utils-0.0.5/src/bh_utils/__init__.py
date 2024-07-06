import logging

__version__ = "0.0.1"

BH_TEMPLATE_FILE_NOT_FOUND_MSG = "Template {} cannot be found."

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
