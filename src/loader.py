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

        # Se comprueba si existen credenciales. En caso de que no haya se piden.
        if credentials["username"] is None or credentials["password"] is None:
            self.logger.info("Faltan credenciales en el fichero de credenciales. Pidiendo al usuario...")
            username = input("Username: ")
            password = input("Password: ")
            # os.system("cls" if os.name == "nt" else "clear")
            self.logger.info("Regenerando fichero de credenciales...")
            self.set_credentials(username, password)
            credentials["username"] = username
            credentials["password"] = password

        # Se quitan los nulos del calendario:
        config["schedule"] = utils.remove_dict_nones(config["schedule"])

        # Se parsea el texto del caldenario para que quede homogeneo:
        schedule = config["schedule"]
        for day in schedule.keys():
            h = schedule[day].split(":")[0].zfill(2)
            m = schedule[day].split(":")[1].zfill(2)
            schedule[day] = f"{h}:{m}"

        return config, credentials

    def set_credentials(self, username, password, credentials_path=const.DEFAULT_CREDENTIALS_FILE):
        yaml.SafeDumper.add_representer(
            type(None),
            lambda dumper, value: dumper.represent_scalar('tag:yaml.org,2002:null', '')
        )
        with open(credentials_path, "w") as f:
            yaml.safe_dump({"username": username, "password": password}, f, sort_keys=False)

    def set_schedule(self, schedule, config_path=const.DEFAULT_CONFIG_FILE):
        empty_schedule = dict.fromkeys(const.WEEK_DAYS)
        yaml.SafeDumper.add_representer(
            type(None),
            lambda dumper, value: dumper.represent_scalar('tag:yaml.org,2002:null', '')
        )
        with open(config_path, "w") as f:
            yaml.safe_dump({'schedule': empty_schedule | schedule}, f, sort_keys=False)
