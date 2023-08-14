import os
from pathlib import Path
from src import const, log, driver, loader, utils


def run():

    logger = log.configureLogger(__name__, save_log=False)
    myloader = loader.Loader(logger=logger)
    const.recalculatePaths(os.getcwd())

    config_items_restored = []
    if not os.path.isdir(const.CONFIG_FOLDER):
        Path(const.CONFIG_FOLDER).mkdir(exist_ok=True)
    if not os.path.exists(const.DEFAULT_CONFIG_FILE):
        utils.create_default_config_file(logger=logger)
        config_items_restored.append("config")
    if not os.path.exists(const.DEFAULT_CREDENTIALS_FILE):
        utils.create_default_credentials_file(logger=logger)
        config_items_restored.append("credentials")
    if not os.path.exists(const.DEFAULT_MANGALIST_FILE):
        utils.create_default_mangalist_file(logger=logger)
        config_items_restored.append("mangalist")
    if len(config_items_restored) > 0:
        logger.info("se han restaurado los siguientes archivos: " + ", ".join(config_items_restored) + ". Por favor, edítelos si es necesario y vuelva a ejecutar el programa.")
        return

    config, credentials, mangalist = myloader.load_config()
    config, temp_folder, save_folder = utils.sanitize_config(config, logger=logger)
    credentials = utils.sanitize_credentials(credentials, logger=logger)
    mangalist = utils.sanitize_mangalist(mangalist, logger=logger)

    browser = driver.MyDriver(logger, sandbox=False)
    browser.navigate_to_home()

    if config["login"] is True:
        if credentials is not None:
            browser.login(credentials["username"], credentials["password"], remember_me=False)
        else:
            logger.warning("No se han encontrado credenciales. No se iniciará sesión.")

    if config["show_volumes"] is False:
        logger.info("No se mostrarán los volúmenes debido a la configuración, lo que conlleva que los capítulos se encuentren separados sin crear carpetas para cada volumen.")

    for manga in mangalist:
        if manga["url"] is None:
            if manga["name"] is not None:
                logger.error(f"No se ha especificado la URL del manga {manga['name']}. Se omitirá este manga.")
            continue

        # Descarga de imágenes
        downloaded_correctly = browser.download_manga(manga_name=manga["name"], manga_url=manga["url"],
                                                      first_chapter=manga["first_chapter"],
                                                      last_chapter=manga["last_chapter"],
                                                      trim_first_pages=manga["trim_first_pages"],
                                                      trim_last_pages=manga["trim_last_pages"],
                                                      temp_folder=temp_folder)
        if not downloaded_correctly:
            logger.error("Ha habido un problema en la descarga, se omitirá este manga.")
            continue

        # Conversión a PDF
        logger.info("Convirtiendo a PDF...")
        converted_correctly = utils.convert_to_pdf(manga_name=manga["name"],
                                                   show_volumes=config["show_volumes"],
                                                   separate_chapters=config["separate_chapters"],
                                                   volume_folders=config["volume_folders"],
                                                   temp_folder=temp_folder, save_folder=save_folder)
        if converted_correctly:
            logger.info("Convertido a PDF correctamente.")
        else:
            logger.error("Ha habido un error en la conversión a PDF.")

        # Borrado de imágenes si se solicita
        if config["delete_images"] is True:
            utils.delete_files(manga_name=manga["name"], folder=temp_folder)
            logger.info("Las imágenes descargadas han sido borradas.")

    browser.close()
    logger.info("Todas las tareas han finalizado correctamente.")


if __name__ == "__main__":
    run()
