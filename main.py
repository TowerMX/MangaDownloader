import os
from src import const, log, driver, loader, utils


def run():

    logger = log.configureLogger(__name__)

    const.recalculatePaths(os.getcwd())
    myloader = loader.Loader()
    config, credentials = myloader.load_config()

    browser = driver.MyDriver(logger, sandbox=True)
    browser.login(credentials["username"], credentials["password"])
    daily_wods = browser.get_all_wods()
    failed_trains = browser.sign_up_for_training(config["schedule"])

    browser.close()


if __name__ == "__main__":
    run()
