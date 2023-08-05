import os

ROOT_PATH = ""

FILES_NAME = "files"
FILES_PATH = os.path.join(ROOT_PATH, FILES_NAME)

LINUX_FOLDER = "linux"
LINUX_DRIVER = "chromedriver"

LINUX_FOLDER_PATH = os.path.join(FILES_PATH, LINUX_FOLDER)
LINUX_DRIVER_PATH = os.path.join(LINUX_FOLDER_PATH, LINUX_DRIVER)

WINDOWS_FOLDER = "win"
WINDOWS_DRIVER = "chromedriver.exe"

WINDOWS_FOLDER_PATH = os.path.join(FILES_PATH, WINDOWS_FOLDER)
WINDOWS_DRIVER_PATH = os.path.join(WINDOWS_FOLDER_PATH, WINDOWS_DRIVER)

LOG_FOLDER = os.path.join(ROOT_PATH, "log")
DEFAULT_LOG_FILE = "main"

CONFIG_FOLDER = os.path.join(ROOT_PATH, "config")
DEFAULT_CREDENTIALS_FILE = os.path.join(CONFIG_FOLDER, "credentials.yaml")
DEFAULT_CONFIG_FILE = os.path.join(CONFIG_FOLDER, "config.yaml")

DEFAULT_ACTION_SLEEP_TIME = 0.5  # seconds
DEFAULT_BROWSE_SLEEP_TIME = 3  # seconds

# DRIVER CONSTANTS

LOGIN_URL = "user/"

LOGIN_USERNAME_BOX_ID = "body_body_body_body_IoEmail"
LOGIN_PASSWORD_BOX_ID = "body_body_body_body_IoPassword"
LOGIN_SUBMIT_BOX_ID = "body_body_body_body_CtlEntrar"

SCHEDULE_URL = "athlete/reservas.aspx"
SCHEDULE_WOD_BOX_CSS_ID = "button[data-id='1']"
SCHEDULE_PIXELS_TO_SCROLL_UP = 100
SCHEDULE_TIME_BETWEEN_DAYS = 864000000000
SCHEDULE_OPEN_BOX_TEXT = "Open Box"
SCHEDULE_BUTTON_TRAINING_TEXT = "Entrenar"

WOD_POPUP_ID = "te1"
WOD_CLOSE_POPUP_CLASS = "fancybox-item fancybox-close"

WEEK_DAYS = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]


def recalculatePaths(root_path):
    global ROOT_PATH, FILES_PATH, LINUX_FOLDER_PATH, LINUX_DRIVER_PATH, WINDOWS_FOLDER_PATH, WINDOWS_DRIVER_PATH, LOG_FOLDER

    ROOT_PATH = root_path

    FILES_PATH = os.path.join(ROOT_PATH, FILES_NAME)

    LINUX_FOLDER_PATH = os.path.join(FILES_PATH, LINUX_FOLDER)
    LINUX_DRIVER_PATH = os.path.join(LINUX_FOLDER_PATH, LINUX_DRIVER)

    WINDOWS_FOLDER_PATH = os.path.join(FILES_PATH, WINDOWS_FOLDER)
    WINDOWS_DRIVER_PATH = os.path.join(WINDOWS_FOLDER_PATH, WINDOWS_DRIVER)

    LOG_FOLDER = os.path.join(ROOT_PATH, "log")
