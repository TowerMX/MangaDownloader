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
        try:
            with open(config_path, "r", encoding="utf8") as f:
                config = yaml.safe_load(f)
        except Exception:
            self.logger.error("Error al intentar leer el archivo config/config.yaml. Comprueba que haya un espacio tras los dos puntos y que se ajuste al formato del README. En caso necesario, borra el archivo y será restaurado correctamente.")
        try:
            with open(credentials_path, "r", encoding="utf8") as f:
                credentials = yaml.safe_load(f)
        except Exception:
            self.logger.error("Error al intentar leer el archivo config/credentials.yaml. Comprueba que haya un espacio tras los dos puntos y que se ajuste al formato del README. En caso necesario, borra el archivo y será restaurado correctamente.")
        try:
            with open(mangalist_path, "r", encoding="utf8") as f:
                mangalist = yaml.safe_load(f)
        except Exception:
            self.logger.error("Error al intentar leer el archivo config/mangalist.yaml. Comprueba que haya un espacio tras los dos puntos y que se ajuste al formato del README. En caso necesario, borra el archivo y será restaurado correctamente.")

        # Se comprueba si existen credenciales y si están corruptas. En caso de que no haya se deja vacío.
        try:
            if credentials["username"] is None or credentials["password"] is None:
                credentials = None
        except KeyError:
            utils.create_default_credentials_file()
            self.logger.warning("El fichero de credenciales está dañado y ha sido regenerado.")
            credentials = None

        return config, credentials, mangalist
