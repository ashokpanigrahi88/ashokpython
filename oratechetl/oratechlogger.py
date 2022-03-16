import logging.config
import logging.handlers
import os
from . import logger_conf as conf

FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOGGER_LEVEL_DEFAULT = os.environ.get("ORATECH_UTILLOG_LEVEL",conf.LOGGER_LEVEL['INFO'])
logging.basicConfig(level=LOGGER_LEVEL_DEFAULT, format=FORMAT)
logging.config.dictConfig(conf.LOGGING_CONFIG)

class OneLineExceptionFormatter(logging.Formatter):
    def formatException(self, exc_info):
        result = super().formatException(exc_info)
        return repr(result)

    def format(self, record):
        result = super().format(record)
        if record.exc_text:
            result = result.replace("\n", "")
        return result

# Create a custom logger
log = logging.getLogger(__name__)

c_handler = logging.StreamHandler()
formatter = logging.Formatter(FORMAT)
#OneLineExceptionFormatter(logging.BASIC_FORMAT)
c_handler.setFormatter(formatter)
c_root = log
c_root.setLevel(LOGGER_LEVEL_DEFAULT)
c_root.addHandler(c_handler)
root = log
root.setLevel(LOGGER_LEVEL_DEFAULT)
root.addHandler(c_handler)

# Create handlers
f_handler = logging.handlers.WatchedFileHandler(conf.LOG_FILES['default'])

# Create formatters and add it to handlers
c_format = logging.Formatter(FORMAT)
f_format = logging.Formatter(FORMAT)
#OneLineExceptionFormatter(logging.BASIC_FORMAT)
f_handler.setFormatter(f_format)

# Add handlers to the logger
log.addHandler(c_handler)
log.addHandler(f_handler)

log.info('testing')
log.warning('testing')