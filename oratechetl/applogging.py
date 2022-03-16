import logging

# Set up the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Getting some docs...")
docs = {'Ben Stokes': 37.8, 'Joe Root': 47.7}
logger.info("Doc count %s", len(docs))
logger.info("Finished")