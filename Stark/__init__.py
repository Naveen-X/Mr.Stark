import logging
from tglogging import TelegramLogHandler

logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        TelegramLogHandler(
            token="1863795995:AAFrgmiZSE5xVWFyanI1qwDtVAiF2mrqDv0",
            log_chat_id=-1001491739934,
            update_interval=2,
            minimum_lines=1,
            pending_logs=200000),
        logging.StreamHandler(),
        logging.FileHandler(
            'log.txt')
    ]
)

logger = logging.getLogger(__name__)

logger.info("live log streaming to telegram.")
