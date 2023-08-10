import os
import logging
from . import const


def configureLogger(name, save_log=False):

    log_file = const.DEFAULT_LOG_FILE + ".log"

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "[%(levelname)s] - %(asctime)s - %(name)s - : %(message)s"
    )

    # "[%(levelname)s] - %(asctime)s - %(name)s - : %(message)s in %(pathname)s:%(lineno)d"

    if save_log:
        if not os.path.exists(const.LOG_FOLDER):
            os.makedirs(const.LOG_FOLDER)
        fh = logging.FileHandler(os.path.join(const.LOG_FOLDER, log_file))
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger
