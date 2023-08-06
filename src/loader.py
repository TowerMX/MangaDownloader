import yaml
from . import const, utils, log


class Loader:
    def __init__(self):
        self.logger = log.configureLogger(__name__)

    def load_config(
            self,
            config_path=const.DEFAULT_CONFIG_FILE,
            credentials_path=const.DEFAULT_CREDENTIALS_FILE,
            mangalist_path=const.DEFAULT_MANGALIST_FILE,
            temp_path=const.DEFAULT_TEMP_FOLDER,
            save_path=const.DEFAULT_SAVE_FOLDER,
    ):
        # Se carga la información
        with open(config_path, "r") as f1:
            config = yaml.safe_load(f1)
        with open(credentials_path, "r") as f2:
            credentials = yaml.safe_load(f2)
        with open(mangalist_path, "r") as f3:
            mangalist = yaml.safe_load(f3)

        if config["temp_path"] is not None:
            temp_path = config["temp_path"]
        if config["save_path"] is not None:
            save_path = config["save_path"]

        # Se comprueba si existen credenciales. En caso de que no haya se deja vacío.
        if credentials["username"] is None or credentials["password"] is None:
            credentials = None

        return config, credentials, mangalist, temp_path, save_path

    def set_credentials(self, username, password, credentials_path=const.DEFAULT_CREDENTIALS_FILE):
        yaml.SafeDumper.add_representer(
            type(None),
            lambda dumper, value: dumper.represent_scalar('tag:yaml.org,2002:null', '')
        )
        with open(credentials_path, "w") as f:
            yaml.safe_dump({"username": username, "password": password}, f, sort_keys=False)
        self.logger.info("Credenciales guardadas correctamente.")
