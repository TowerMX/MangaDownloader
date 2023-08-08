import os
from src import const, log, driver, loader, utils


def run():

    logger = log.configureLogger(__name__)

    const.recalculatePaths(os.getcwd())
    myloader = loader.Loader()
    config, credentials, mangalist, temp_folder, save_folder = myloader.load_config()

    browser = driver.MyDriver(logger, sandbox=False)
    browser.navigate_to_home()

    if config["login"] is True:
        if credentials is not None:
            browser.login(credentials["username"], credentials["password"], remember_me=config["remember_me"])
        else:
            logger.warning("No se han encontrado credenciales. No se iniciará sesión.")

    for manga in mangalist:
        downloaded_correctly = browser.download_manga(manga["name"], manga["url"], manga["first_chapter"], manga["last_chapter"], temp_folder=temp_folder)
        if not downloaded_correctly:
            continue
        logger.info("Convirtiendo a PDF...")
        utils.convert_to_pdf(manga["name"], temp_folder=temp_folder, save_folder=save_folder)
        logger.info("Convertido a PDF correctamente.")
        if config["delete_images"] is True:
            utils.delete_images(manga["name"], temp_folder=temp_folder)
            logger.info("Las imágenes descargadas han sido borradas.")

    logger.info("Cerrando navegador.")
    browser.close()


if __name__ == "__main__":
    run()
