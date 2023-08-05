import os
import logging
from . import const


def configureLogger(name):
    handleLogFolder(const.LOG_FOLDER)

    log_file = const.DEFAULT_LOG_FILE + ".log"

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "[%(levelname)s] - %(asctime)s - %(name)s - : %(message)s"
    )

    # "[%(levelname)s] - %(asctime)s - %(name)s - : %(message)s in %(pathname)s:%(lineno)d"

    fh = logging.FileHandler(os.path.join(const.LOG_FOLDER, log_file))
    ch = logging.StreamHandler()

    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger


def handleLogFolder(path):
    if not os.path.exists(path):
        os.makedirs(path)
