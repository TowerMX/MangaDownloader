import os
from pathlib import Path
from src import const, log, driver, loader, utils


def run():

    logger = log.configureLogger(__name__, save_log=False)
    myloader = loader.Loader(logger)
    const.recalculatePaths(os.getcwd())

    config_regenerated = False
    if not os.path.isdir(const.CONFIG_FOLDER):
        Path(const.CONFIG_FOLDER).mkdir(exist_ok=True)
        config_regenerated = True
    if not os.path.exists(const.DEFAULT_CONFIG_FILE):
        utils.create_default_config_file()
        config_regenerated = True
    if not os.path.exists(const.DEFAULT_CREDENTIALS_FILE):
        utils.create_default_credentials_file()
        config_regenerated = True
    if not os.path.exists(const.DEFAULT_MANGALIST_FILE):
        utils.create_default_mangalist_file()
        config_regenerated = True
    if config_regenerated:
        logger.info(
            "Se han generado los archivos de configuración por defecto. Por favor, edítelos y vuelva a ejecutar el programa.")
        return

    config, credentials, mangalist, temp_folder, save_folder = myloader.load_config()
    try:
        const.set_language(language=config["language"], logger=logger)
    except KeyError:
        const.set_language(language="es")

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

    try:
        len(mangalist)
    except TypeError:
        logger.warning("La lista de mangas está vacía.")
        return

    browser = driver.MyDriver(logger, sandbox=False)
    browser.navigate_to_home()

    if config["login"] is True:
        if credentials is not None:
            browser.login(credentials["username"], credentials["password"], remember_me=False)
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

    browser.close()
    logger.info("Todas las tareas han finalizado correctamente.")


if __name__ == "__main__":
    run()
