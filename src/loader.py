import yaml
from . import const, log, utils


class Loader:
    def __init__(self, logger=log.configureLogger(__name__)):
        self.logger = logger

    def load_config(
            self,
            config_path=const.DEFAULT_CONFIG_FILE,
            credentials_path=const.DEFAULT_CREDENTIALS_FILE,
            mangalist_path=const.DEFAULT_MANGALIST_FILE,
    ):
        # Se carga la información
        with open(config_path, "r") as f1:
            config = yaml.safe_load(f1)
        with open(credentials_path, "r") as f2:
            credentials = yaml.safe_load(f2)
        with open(mangalist_path, "r") as f3:
            mangalist = yaml.safe_load(f3)

        # Se comprueba si existen credenciales y si están corruptas. En caso de que no haya se deja vacío.
        try:
            if credentials["username"] is None or credentials["password"] is None:
                credentials = None
        except KeyError:
            utils.create_default_credentials_file()
            self.logger.warning("El fichero de credenciales está dañado y ha sido regenerado.")
            credentials = None

        return config, credentials, mangalist
