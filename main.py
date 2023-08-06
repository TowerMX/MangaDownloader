import os
from src import const, log, driver, loader, utils


def run():

    logger = log.configureLogger(__name__)

    const.recalculatePaths(os.getcwd())
    myloader = loader.Loader()
    config, credentials, mangalist, temp_path, save_path = myloader.load_config()

    browser = driver.MyDriver(logger, sandbox=False)
    browser.navigate_to_home()

    if config["login"] is True:
        if credentials is not None:
            browser.login(credentials["username"], credentials["password"], remember_me=config["remember_me"])
        else:
            logger.warning("No se han encontrado credenciales. No se iniciará sesión.")

    '''
    for manga in mangalist:
        browser.download_manga(manga["name"], manga["url"], manga["first_chapter"], manga["last_chapter"], temp_path)
        utils.convert_to_pdf(manga["name"], temp_path, save_path)
        utils.delete_images(manga["name"], temp_path)
    '''

    logger.info("Cerrando navegador.")
    browser.close()


if __name__ == "__main__":
    run()
