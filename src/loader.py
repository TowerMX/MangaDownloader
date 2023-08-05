import yaml
from . import const, utils, log


class Loader:
    def __init__(self):
        self.logger = log.configureLogger(__name__)

    def load_config(
            self,
            config_path=const.DEFAULT_CONFIG_FILE,
            credentials_path=const.DEFAULT_CREDENTIALS_FILE,
    ):
        # Se carga la información
        with open(config_path, "r") as f1:
            config = yaml.safe_load(f1)
        with open(credentials_path, "r") as f2:
            credentials = yaml.safe_load(f2)

        # Se comprueba si existen credenciales. En caso de que no haya se deja vacío.
        if credentials["username"] is None or credentials["password"] is None:
            credentials = None

        return config, credentials

    def set_credentials(self, username, password, credentials_path=const.DEFAULT_CREDENTIALS_FILE):
        yaml.SafeDumper.add_representer(
            type(None),
            lambda dumper, value: dumper.represent_scalar('tag:yaml.org,2002:null', '')
        )
        with open(credentials_path, "w") as f:
            yaml.safe_dump({"username": username, "password": password}, f, sort_keys=False)
        self.logger.info("Credenciales guardadas correctamente.")
