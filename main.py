import os
from src import const, log, driver, loader, utils


def run():

    logger = log.configureLogger(__name__)

    const.recalculatePaths(os.getcwd())
    myloader = loader.Loader()
    config, credentials = myloader.load_config()

    browser = driver.MyDriver(logger, sandbox=True)

    if credentials is not None:
        browser.login(credentials["username"], credentials["password"])

    browser.close()


if __name__ == "__main__":
    run()
