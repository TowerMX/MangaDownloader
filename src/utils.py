from pathlib import Path
from PIL import Image
import yaml
import shutil
import os
from . import const


def delete_files(manga_name, folder):
    shutil.rmtree(rf"{folder}\{manga_name}", ignore_errors=True)


def convert_to_pdf(manga_name, show_volumes=True, separate_chapters=True, volume_folders=False,
                   temp_folder=const.DEFAULT_TEMP_FOLDER, save_folder=const.DEFAULT_SAVE_FOLDER):
    try:
        # Crea carpeta del manga
        Path(rf"{save_folder}\{manga_name}").mkdir(exist_ok=True)
        if not show_volumes:
            separate_chapters=True
            volume_folders=False
        for volume in os.scandir(rf"{temp_folder}\{manga_name}"):
            if not volume.is_dir():
                continue
            # Crea carpeta del volumen si se solicita
            if volume_folders:
                Path(rf"{save_folder}\{manga_name}\{volume.name}").mkdir(exist_ok=True)

            if volume.name == "Oneshot":
                images_folder = rf"{temp_folder}\{manga_name}\{volume.name}"
                pdf_path = rf"{save_folder}\{manga_name}\{volume.name}.pdf"
                _images_to_pdf(images_folder, pdf_path)
            elif not show_volumes or volume.name == "No volumes":
                images_folder_list = []
                for chapter in os.scandir(rf"{temp_folder}\{manga_name}\{volume.name}"):
                    if not chapter.is_dir():
                        continue
                    images_folder = rf"{temp_folder}\{manga_name}\{volume.name}\{chapter.name}"
                    if separate_chapters:
                        if volume_folders:
                            pdf_path = rf"{save_folder}\{manga_name}\{volume.name}\{chapter.name}.pdf"
                        else:
                            pdf_path = rf"{save_folder}\{manga_name}\{chapter.name}.pdf"
                        _images_to_pdf([images_folder], pdf_path)
                    else:
                        images_folder_list.append(images_folder)
                if not separate_chapters:
                    pdf_path = rf"{save_folder}\{manga_name}\{volume.name}.pdf"
                    _images_to_pdf(images_folder_list, pdf_path)
            else:
                images_folder_list = []
                for chapter in os.scandir(rf"{temp_folder}\{manga_name}\{volume.name}"):
                    if not chapter.is_dir():
                        continue
                    images_folder = rf"{temp_folder}\{manga_name}\{volume.name}\{chapter.name}"
                    if separate_chapters:
                        if volume_folders:
                            pdf_path = rf"{save_folder}\{manga_name}\{volume.name}\{chapter.name}.pdf"
                        else:
                            pdf_path = rf"{save_folder}\{manga_name}\{volume.name}, {chapter.name}.pdf"
                        _images_to_pdf([images_folder], pdf_path)
                    else:
                        images_folder_list.append(images_folder)
                if not separate_chapters:
                    pdf_path = rf"{save_folder}\{manga_name}\{volume.name}.pdf"
                    _images_to_pdf(images_folder_list, pdf_path)
        return True
    except Exception:
        return False


def _images_to_pdf(images_folder_list, pdf_path):
    full_list = []
    for images_folder in images_folder_list:
        images = {}
        for page in os.scandir(images_folder):
            if page.is_dir():
                continue
            # Se convierte a RGB, el tamaño final se reduce en 10 veces
            images[int(page.name.split(".")[0])] = Image.open(page.path).convert('RGB')
        sorted_images = sorted(images.items())
        image_list = [image_tuple[1] for image_tuple in sorted_images]
        full_list.extend(image_list)
    if len(full_list) > 1:
        full_list[0].save(
            pdf_path, "PDF", resolution=100.0, save_all=True, append_images=full_list[1:]
        )
    elif len(full_list) > 0:
        full_list[0].save(
            pdf_path, "PDF", resolution=100.0
        )


def sanitize_config(config, config_path=const.DEFAULT_CONFIG_FILE, logger=None):
    config = const.CONFIG_TEMPLATE | config
    for key in config.keys():
        if key not in const.CONFIG_TEMPLATE.keys():
            config.pop(key)
            if logger is not None:
                logger.warning(f"El campo config/{key} no es utilizado por este programa. Revise el README.")

    if config["language"] in const.VALID_LANGUAGES:
        const.set_language(language=config["language"], logger=logger)
    else:
        const.set_language(language="es", logger=logger)
        if logger is not None:
            logger.warning(f"El valor de config/language no es válido. Se utilizará el idioma por defecto: español.")

    config["login"] = _parse_boolean(config["login"], const.CONFIG_TEMPLATE["login"],
                                     name="config/login", logger=logger)
    config["delete_images"] = _parse_boolean(config["delete_images"], const.CONFIG_TEMPLATE["delete_images"],
                                             name="config/delete_images", logger=logger)
    config["show_volumes"] = _parse_boolean(config["show_volumes"], const.CONFIG_TEMPLATE["show_volumes"],
                                            name="config/show_volumes", logger=logger)
    config["separate_chapters"] = _parse_boolean(config["separate_chapters"], const.CONFIG_TEMPLATE["separate_chapters"],
                                                 name="config/separate_chapters", logger=logger)
    config["volume_folders"] = _parse_boolean(config["volume_folders"], const.CONFIG_TEMPLATE["volume_folders"],
                                              name="config/volume_folders", logger=logger)

    if config["temp_path"] is not None:
        temp_folder = config["temp_path"]
        print(temp_folder)
        try:
            Path(temp_folder).mkdir(exist_ok=True)
        except (FileNotFoundError, Exception):
            if logger is not None:
                logger.error("La ubicación de la carpeta de descarga no es válida o no existe el directorio que la contiene. Se usará la carpeta por defecto.")
            temp_folder = const.DEFAULT_TEMP_FOLDER
    else:
        temp_folder = const.DEFAULT_TEMP_FOLDER
    if config["save_path"] is not None:
        save_folder = config["save_path"]
        try:
            Path(save_folder).mkdir(exist_ok=True)
        except (FileNotFoundError, Exception):
            if logger is not None:
                logger.error("La ubicación de la carpeta de guardado no es válida o no existe el directorio que la contiene. Se usará la carpeta por defecto.")
            save_folder = const.DEFAULT_SAVE_FOLDER
    else:
        save_folder = const.DEFAULT_SAVE_FOLDER

    # Para que guarde los valores como "yes" o "no" en vez de True o False
    config_saved = config.copy()
    for (key, value) in config_saved.items():
        if value is True:
            config_saved[key] = "yes"
        elif value is False:
            config_saved[key] = "no"

    set_yaml(config_saved, config_path, logger=logger)

    # No debería hacer falta quitar las comillas así ya que se supone que ya se hace en set_yaml, pero es necesario
    with open(config_path, "r") as f:
        config_text = f.read()
    config_text = config_text.replace(": 'yes'", ": yes")
    config_text = config_text.replace(": 'no'", ": no")
    with open(config_path, "w") as f:
        f.write(config_text)

    return config, temp_folder, save_folder


def sanitize_credentials(credentials, credentials_path=const.DEFAULT_CREDENTIALS_FILE, logger=None):
    if credentials is not None:
        credentials = const.CREDENTIALS_TEMPLATE | credentials
    else:
        credentials = const.CREDENTIALS_TEMPLATE
    for key in credentials.keys():
        if key not in const.CREDENTIALS_TEMPLATE.keys():
            credentials.pop(key)
            if logger is not None:
                logger.warning(f"El campo credentials/{key} no es utilizado por este programa. Revise el README.")
            continue
        if credentials[key] is None:
            continue
        elif not isinstance(credentials[key], str):
            if logger is not None:
                logger.warning(f"El valor de credentials/{key} no es adecuado y ha sido borrado.")
            credentials[key] = None

    set_yaml(credentials, credentials_path, logger=logger)

    if credentials["username"] is None or credentials["password"] is None:
        credentials = None

    return credentials


def sanitize_mangalist(mangalist, mangalist_path=const.DEFAULT_MANGALIST_FILE, logger=None):
    if isinstance(mangalist, list):
        for (index, manga) in enumerate(mangalist):
            if not isinstance(manga, dict):
                mangalist[index] = const.MANGA_TEMPLATE
                if logger is not None:
                    logger.warning(f"El manga nº {index+1} no es válido. Se cambiará por la plantilla por defecto.")
                continue
            manga = const.MANGA_TEMPLATE | manga
            for key in manga.keys():
                if key not in const.MANGA_TEMPLATE.keys():
                    manga.pop(key)
                    if logger is not None:
                        logger.warning(f"El campo mangalist/{manga['name']}/{key} no es utilizado por este programa. Revise el README.")
                    continue

            if manga["name"] is None or manga["name"] == "":
                if manga["name"] is not None:
                    manga["name"] = None
                if logger is not None:
                    logger.warning(f"El nombre del manga nº {index+1} está vacío. Se utilizará el título de la página web.")
            elif isinstance(manga["name"], (int, float, bool)):
                manga["name"] = str(manga["name"])
            elif not isinstance(manga["name"], str):
                manga["name"] = None
                if logger is not None:
                    logger.warning(f"El nombre del manga nº {index+1} no es válido. Se utilizará el título de la página web.")
            else:
                manga["name"] = parse_title(manga["name"])

            if manga["url"] is None or manga["url"] == "":
                if manga["url"] is not None:
                    manga["url"] = None
                if logger is not None:
                    if manga["name"] is not None:
                        logger.warning(f"La URL del manga {manga['name']} está vacía. No se descargará este manga.")
                    else:
                        logger.warning(f"La URL del manga nº {index+1} está vacía. No se descargará este manga.")
            elif not isinstance(manga["name"], str):
                manga["url"] = None
                if logger is not None:
                    if manga["name"] is not None:
                        logger.warning(f"La URL del manga {manga['name']} no es válida. No se descargará este manga.")
                    else:
                        logger.warning(f"La URL del manga nº {index+1} no es válida. No se descargará este manga.")

            if not isinstance(manga["first_chapter"], (int, float)) and manga["first_chapter"] != "first":
                manga["first_chapter"] = const.MANGA_TEMPLATE["first_chapter"]
                if logger is not None:
                    if manga["name"] is not None:
                        logger.warning(f"El valor de mangalist/{manga['name']}/first_chapter no es válido. Se utilizará el valor por defecto: {const.MANGA_TEMPLATE['first_chapter']}.")
                    else:
                        logger.warning(f"El valor de mangalist/manga nº {index+1}/first_chapter no es válido. Se utilizará el valor por defecto: {const.MANGA_TEMPLATE['first_chapter']}.")

            if not isinstance(manga["last_chapter"], (int, float)) and manga["last_chapter"] != "last":
                manga["last_chapter"] = const.MANGA_TEMPLATE["last_chapter"]
                if logger is not None:
                    if manga["name"] is not None:
                        logger.warning(f"El valor de mangalist/{manga['name']}/last_chapter no es válido. Se utilizará el valor por defecto: {const.MANGA_TEMPLATE['last_chapter']}.")
                    else:
                        logger.warning(f"El valor de mangalist/manga nº {index+1}/last_chapter no es válido. Se utilizará el valor por defecto: {const.MANGA_TEMPLATE['last_chapter']}.")

            if not isinstance(manga["trim_first_pages"], int) or manga["trim_first_pages"] < 0:
                manga["trim_first_pages"] = const.MANGA_TEMPLATE["trim_first_pages"]
                if logger is not None:
                    if manga["name"] is not None:
                        logger.warning(f"El valor de mangalist/{manga['name']}/trim_first_pages no es válido. Se utilizará el valor por defecto: {const.MANGA_TEMPLATE['trim_first_pages']}.")
                    else:
                        logger.warning(f"El valor de mangalist/manga nº {index+1}/trim_first_pages no es válido. Se utilizará el valor por defecto: {const.MANGA_TEMPLATE['trim_first_pages']}.")

            if not isinstance(manga["trim_last_pages"], int) or manga["trim_last_pages"] < 0:
                manga["trim_last_pages"] = const.MANGA_TEMPLATE["trim_last_pages"]
                if logger is not None:
                    if manga["name"] is not None:
                        logger.warning(f"El valor de mangalist/{manga['name']}/trim_last_pages no es válido. Se utilizará el valor por defecto: {const.MANGA_TEMPLATE['trim_last_pages']}.")
                    else:
                        logger.warning(f"El valor de mangalist/manga nº {index+1}/trim_last_pages no es válido. Se utilizará el valor por defecto: {const.MANGA_TEMPLATE['trim_last_pages']}.")

        mangalist[index] = manga
    else:
        mangalist = []
        create_default_mangalist_file()
        if logger is not None:
            logger.error("La lista de mangas está vacía o los datos están corruptos. Se ha creado un nuevo archivo mangalist.")
        return mangalist

    set_yaml(mangalist, mangalist_path, logger=logger)

    return mangalist


def create_default_config_file(logger=None):
    set_yaml(const.CONFIG_TEMPLATE, const.DEFAULT_CONFIG_FILE, logger=logger)
    # No debería hacer falta quitar las comillas así ya que se supone que ya se hace en set_yaml, pero es necesario
    with open(const.DEFAULT_CONFIG_FILE, "r") as f:
        config_text = f.read()
    config_text = config_text.replace(": 'yes'", ": yes")
    config_text = config_text.replace(": 'no'", ": no")
    with open(const.DEFAULT_CONFIG_FILE, "w") as f:
        f.write(config_text)


def create_default_credentials_file(logger=None):
    set_yaml(const.CREDENTIALS_TEMPLATE, const.DEFAULT_CREDENTIALS_FILE, logger=logger)


def create_default_mangalist_file(logger=None):
    set_yaml([const.MANGA_TEMPLATE, const.MANGA_TEMPLATE], const.DEFAULT_MANGALIST_FILE, logger=logger)


def set_yaml(content, path, logger=None):
    try:
        # Deja en blanco en vez de poner none
        yaml.SafeDumper.add_representer(
            type(None),
            lambda dumper, value: dumper.represent_scalar('tag:yaml.org,2002:null', '')
        )
        # Elimina los "punteros" (aliases/anchors) en las listas
        yaml.SafeDumper.ignore_aliases = lambda *args: True
        # No muestra comillas en los strings y cada valor en una línea sin reordenarse
        with open(path, "w") as f:
            yaml.safe_dump(content, f, sort_keys=False, default_style=None, default_flow_style=False)
    except Exception:
        if logger is not None:
            logger.error(f"Ha ocurrido un error al escribir el archivo {path}. Compruebe que el archivo no está abierto en otro programa.")


def parse_title(text):
    for (i, character) in enumerate(const.FORBIDDEN_CHARACTERS):
        text = text.replace(character, const.REPLACING_CHARACTERS[i])
    return text


def _parse_boolean(value, default, name=None, logger=None):
    if value == "yes":
        return True
    elif value == "no":
        return False
    elif not isinstance(value, bool):
        if name is not None and logger is not None:
            logger.warning(f"El valor de {name} no es válido. Se utilizará el valor por defecto: {default}.")
        return _parse_boolean(default, default, name=name, logger=logger)
    return value
