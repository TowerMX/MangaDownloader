import yaml
from . import const, log


class Loader:
    def __init__(self, logger=log.configureLogger(__name__)):
        self.logger = logger

    def load_config(
            self,
            config_path=const.DEFAULT_CONFIG_FILE,
            credentials_path=const.DEFAULT_CREDENTIALS_FILE,
            mangalist_path=const.DEFAULT_MANGALIST_FILE,
            temp_folder=const.DEFAULT_TEMP_FOLDER,
            save_folder=const.DEFAULT_SAVE_FOLDER,
    ):
        # Se carga la información
        with open(config_path, "r") as f1:
            config = yaml.safe_load(f1)
        with open(credentials_path, "r") as f2:
            credentials = yaml.safe_load(f2)
        with open(mangalist_path, "r") as f3:
            mangalist = yaml.safe_load(f3)

        try:
            if config["temp_path"] is not None:
                temp_folder = config["temp_path"]
        except KeyError:
            pass
        try:
            if config["save_path"] is not None:
                save_folder = config["save_path"]
        except KeyError:
            pass

        # Se comprueba si existen credenciales. En caso de que no haya se deja vacío.
        if credentials["username"] is None or credentials["password"] is None:
            credentials = None

        return config, credentials, mangalist, temp_folder, save_folder

    def set_credentials(self, username, password, credentials_path=const.DEFAULT_CREDENTIALS_FILE):
        yaml.SafeDumper.add_representer(
            type(None),
            lambda dumper, value: dumper.represent_scalar('tag:yaml.org,2002:null', '')
        )
        with open(credentials_path, "w") as f:
            yaml.safe_dump({"username": username, "password": password}, f, sort_keys=False)
        self.logger.info("Credenciales guardadas correctamente.")
