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
DEFAULT_CONFIG_FILE = os.path.join(CONFIG_FOLDER, "config.yaml")
DEFAULT_CREDENTIALS_FILE = os.path.join(CONFIG_FOLDER, "credentials.yaml")
DEFAULT_MANGALIST_FILE = os.path.join(CONFIG_FOLDER, "mangalist.yaml")

DEFAULT_TEMP_FOLDER = os.path.join(ROOT_PATH, "temp")
DEFAULT_SAVE_FOLDER = os.path.join(ROOT_PATH, "mangas")

VOLUME_FOLDER_STRING = "Volumen"
CHAPTER_FOLDER_STRING = "Capítulo"


# DRIVER CONSTANTS

HOME_URL = "https://mangadex.org"

AVATAR_ID = "avatar"
SIGN_IN_BUTTON_CLASS = "mb-2 rounded relative md-btn flex items-center px-3 overflow-hidden primary glow px-4 mb-2"
SIGN_OUT_BUTTON_CLASS = "list__item hover:bg-accent block cursor-pointer rounded relative md-btn flex items-center px-3 overflow-hidden accent text px-4 list__item hover:bg-accent block cursor-pointer"

REGISTER_BUTTON_XPATH = "/html/body/div[1]/div[3]/div[2]/div/div[1]/button[5]"
REGISTER_BUTTON_CSS_SELECTOR = "button.accent:nth-child(8)"
SIGN_IN_BUTTON_XPATH = "/html/body/div[1]/div[3]/div[2]/div/div[1]/button[4]"
SIGN_IN_BUTTON_CSS_SELECTOR = "button.mb-2:nth-child(7)"
SIGN_OUT_BUTTON_XPATH = "/html/body/div[1]/div[3]/div[2]/div/div[1]/button[4]"
SIGN_OUT_BUTTON_CSS_SELECTOR = "button.hover\:bg-accent:nth-child(7)"

LOGIN_USERNAME_BOX_ID = "username"
LOGIN_PASSWORD_BOX_ID = "password"
LOGIN_REMEMBER_ME_BOX_ID = "rememberMe"
LOGIN_SUBMIT_BOX_ID = "kc-login"

MANGA_CHAPTER_CLASS = "reader--meta chapter"
MANGA_CHAPTER_XPATH = "/html/body/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[1]/div[2]/div[1]"
MANGA_CHAPTER_CSS_SELECTOR = "div.reader--meta:nth-child(1)"
MANGA_PAGE_CLASS = "reader--meta page"
MANGA_PAGE_XPATH = "/html/body/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[1]/div[2]/div[2]"
MANGA_PAGE_CSS_SELECTOR = "div.reader--meta:nth-child(2)"
MANGA_IMAGE_CLASS = "img sp limit-width limit-height mx-auto"
MANGA_IMAGE_XPATH = "/html/body/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[2]/div[1]/div/img[1]"
MANGA_IMAGE_CSS_SELECTOR = "img.img:nth-child(1)"

DEFAULT_ACTION_SLEEP_TIME = 0.3  # seconds
DEFAULT_BROWSE_SLEEP_TIME = 3  # seconds
DEFAULT_LOGIN_SLEEP_TIME = 5  # seconds
DEFAULT_PAGE_TURN_SLEEP_TIME = 0.5  # seconds
DEFAULT_CHAPTER_CHANGE_SLEEP_TIME = 1  # seconds


def recalculatePaths(root_path):
    global ROOT_PATH, FILES_PATH, LINUX_FOLDER_PATH, LINUX_DRIVER_PATH, WINDOWS_FOLDER_PATH, WINDOWS_DRIVER_PATH, LOG_FOLDER

    ROOT_PATH = root_path

    FILES_PATH = os.path.join(ROOT_PATH, FILES_NAME)

    LINUX_FOLDER_PATH = os.path.join(FILES_PATH, LINUX_FOLDER)
    LINUX_DRIVER_PATH = os.path.join(LINUX_FOLDER_PATH, LINUX_DRIVER)

    WINDOWS_FOLDER_PATH = os.path.join(FILES_PATH, WINDOWS_FOLDER)
    WINDOWS_DRIVER_PATH = os.path.join(WINDOWS_FOLDER_PATH, WINDOWS_DRIVER)

    LOG_FOLDER = os.path.join(ROOT_PATH, "log")
