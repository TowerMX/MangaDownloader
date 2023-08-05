import os
from src import const, log, driver, loader, utils


def run():

    logger = log.configureLogger(__name__)

    const.recalculatePaths(os.getcwd())
    myloader = loader.Loader()
    config, credentials, mangalist = myloader.load_config()

    if config["temp_folder"] is not None:
        temp_path = config["temp_folder"]
    else:
        temp_path = const.DEFAULT_TEMP_FOLDER
    if config["save_folder"] is not None:
        save_path = config["save_folder"]
    else:
        save_path = const.DEFAULT_SAVE_FOLDER

    browser = driver.MyDriver(logger, sandbox=False)

    if config["login"] is True:
        if credentials is not None:
            browser.login(credentials["username"], credentials["password"])
        else:
            logger.warning("No se han encontrado credenciales. No se iniciará sesión.")

    for manga in mangalist:
        browser.download_manga(manga["name"], manga["url"], manga["first_chapter"], manga["last_chapter"], temp_path)
        utils.convert_to_pdf(manga["name"], temp_path, save_path)
        utils.delete_images(manga["name"], temp_path)

    logger.info("Cerrando navegador.")
    browser.close()


if __name__ == "__main__":
    run()
