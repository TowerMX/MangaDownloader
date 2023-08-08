import os
from pathlib import Path
from src import const, log, driver, loader, utils


def run():

    logger = log.configureLogger(__name__)

    const.recalculatePaths(os.getcwd())
    myloader = loader.Loader()
    config, credentials, mangalist, temp_folder, save_folder = myloader.load_config()

    try:
        Path(temp_folder).mkdir(exist_ok=True)
    except FileNotFoundError:
        logger.error("La ubicación de la carpeta de descarga no es válida o no existe el directorio que la contiene.")
        return
    try:
        Path(save_folder).mkdir(exist_ok=True)
    except FileNotFoundError:
        logger.error("La ubicación de la carpeta de guardado no es válida o no existe el directorio que la contiene.")
        return

    browser = driver.MyDriver(logger, sandbox=False)
    browser.navigate_to_home()

    if config["login"] is True:
        if credentials is not None:
            browser.login(credentials["username"], credentials["password"], remember_me=config["remember_me"])
        else:
            logger.warning("No se han encontrado credenciales. No se iniciará sesión.")

    for manga in mangalist:
        # Descarga de imágenes
        downloaded_correctly = browser.download_manga(manga["name"], manga["url"], manga["first_chapter"], manga["last_chapter"], temp_folder=temp_folder)
        if not downloaded_correctly:
            logger.error("Ha habido un problema en la descarga, se omitirá este manga.")
            continue

        # Conversión a PDF
        logger.info("Convirtiendo a PDF...")
        converted_correctly = utils.convert_to_pdf(manga["name"], temp_folder=temp_folder, save_folder=save_folder)
        if converted_correctly:
            logger.info("Convertido a PDF correctamente.")
        else:
            logger.error("Ha habido un error en la conversión a PDF.")

        # Borrado de imágenes si se solicita
        if config["delete_images"] is True:
            utils.delete_files(manga["name"], temp_folder)
            logger.info("Las imágenes descargadas han sido borradas.")

    logger.info("Cerrando navegador.")
    browser.close()


if __name__ == "__main__":
    run()
