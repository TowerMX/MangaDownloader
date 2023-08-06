from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from pathlib import Path
import platform
import time
from . import const, utils


class MyDriver:

    base_url = "https://mangadex.org/"

    def __init__(self, logger, sandbox=False):
        self.logger = logger
        self.sandbox = sandbox
        if self.sandbox:
            self.logger.debug("Modo sandbox activado.")
        self.logger.debug("Inicializando el driver...")
        platform_os = platform.system()

        chrome_options = Options()

        # Set the user agent string to a common browser
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"

        # Set the user agent and other custom headers
        chrome_options.add_argument("user-agent=" + user_agent)
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-setuid-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-accelerated-2d-canvas")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1200")
        chrome_options.add_argument("--hide-scrollbars")

        if platform_os == "Linux":
            driver_path = const.LINUX_DRIVER_PATH
        else:  # platform_os == 'Windows'
            driver_path = const.WINDOWS_DRIVER_PATH

        service = Service(executable_path=driver_path)

        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.logger.debug(f"Se ha inicializado el driver con el os {platform_os}.")


    def login(self, username, password, remember_me=False):
        try:
            # Abre el menú de usuario
            avatar = self.driver.find_element(By.ID, const.AVATAR_ID)
            self._click(avatar)
            # Busca el botón de cerrar sesión
            self.driver.find_element(By.CLASS_NAME, const.SIGN_OUT_BUTTON_CLASS)
            # Si llega a este punto es que ya estaba iniciada la sesión
            self.logger.info("La sesión ya estaba iniciada.")
        except NoSuchElementException:
            # En caso de que no se encuentre, hay que iniciar sesión
            self.logger.info("Comenzando el login...")
            signin_button = self.driver.find_element(By.CLASS_NAME, const.SIGN_IN_BUTTON_CLASS)
            self._click(signin_button)

            self.logger.debug("Encontrando objetos...")
            username_box = self.driver.find_element(By.ID, const.LOGIN_USERNAME_BOX_ID)
            password_box = self.driver.find_element(By.ID, const.LOGIN_PASSWORD_BOX_ID)
            remember_me_box = self.driver.find_element(By.ID, const.LOGIN_REMEMBER_ME_BOX_ID)
            submit_box = self.driver.find_element(By.ID, const.LOGIN_SUBMIT_BOX_ID)

            self.logger.debug("Mandando teclas...")
            self._send_keys(username, username_box)
            self._send_keys(password, password_box)
            if remember_me:
                self._click(remember_me_box)
            self._click(submit_box, sleep_time=const.DEFAULT_LOGIN_SLEEP_TIME)

            self.logger.info("Se ha iniciado sesión correctamente.")


    def download_manga(self, manga_name, manga_url, first_chapter, last_chapter, temp_path=const.DEFAULT_TEMP_FOLDER):
        manga_path = Path(rf"{temp_path}\{manga_name}")
        manga_path.mkdir(exist_ok=True)

        # Volume loop
        while True:

            # Chapter loop
            while True:

                # Page loop
                while True:

                    url = self.driver.current_url
                    url_check = url.split("/")[3]

                    if url_check == "chapter":
                        pass
                    elif url_check == "title":
                        self.logger.info("Se ha llegado al final del manga. Saliendo...")
                        break
                    else:
                        self.logger.error("Error en la URL. Saliendo...")
                        break

                    self._download_page(manga_name, manga_path, temp_path)
                    if self._is_last_page():
                        break
                    self._next_page()
                if self._is_last_chapter():
                    break
                self._next_chapter()


        chapter_element = self.driver.find_element(By.CLASS_NAME, const.MANGA_CHAPTER_CLASS)
        page_element = self.driver.find_element(By.CLASS_NAME, const.MANGA_PAGE_CLASS)

        if chapter_element.text == "Oneshot":
            volume_folder = "Oneshot"
            chapter_folder = "\b"
        else:
            chapter_split = chapter_element.text.split(", ")
            volume = chapter_split[0].split(" ")[1]
            chapter = chapter_split[1].split(" ")[1]
            volume_folder = f"{const.VOLUME_FOLDER_STRING} {volume}"
            chapter_folder = f"{const.CHAPTER_FOLDER_STRING} {chapter}"

        page_split = page_element.text.split(" / ")
        page = page_split[0].split(" ")[1]
        last_page = page_split[1]


        p = Path(rf"{temp_path}\{manga_name}\{volume_folder}\{chapter_folder}")
        p.mkdir(exist_ok=True)


        img = self.driver.find_element(By.CLASS_NAME, const.MANGA_IMAGE_CLASS)
        self._download_image(img, image_number, path)















    def _download_image(self, image_element, image_number, path):
        return None





    def navigate_to_home(self):
        self._navigate(const.HOME_URL)

    def _navigate(self, url, sleep_time=const.DEFAULT_BROWSE_SLEEP_TIME):
        self.driver.get(url)
        self._wait(sleep_time)

    def _page_turn(self, direction="right", sleep_time=const.DEFAULT_PAGE_TURN_SLEEP_TIME):
        actions = ActionChains(self.driver)
        if direction == "right":
            actions.send_keys(Keys.RIGHT)
        elif direction == "left":
            actions.send_keys(Keys.LEFT)
        else:
            raise ValueError(f"Direction {direction} not valid")
        actions.perform()
        self._wait(sleep_time)

    def _wait(self, sleep_time):
        time.sleep(sleep_time)


    def _make_visible(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        self.driver.execute_script(
            f"window.scrollBy(0, -{const.SCHEDULE_PIXELS_TO_SCROLL_UP});"
        )

    def _parse_text(self, text):
        # EXAMPLE = "Wod\nWeightlifting\nSquat snatch\nE2MO2M 10’\n1 x 2 80%\n2 x 2 85%\n2 x 2 90%\nE3MO3M 12’\n1 x 1 95%\n1 x 1 100%\n2 x RM\nSquat snatch\nMax (n) rep(s)\n1RM 2RM 3RM 4RM 5RM 6RM 7RM 8RM 9RM 10RM 11RM 12RM 13RM 14RM 15RM 16RM 17RM 18RM 19RM 20RM\n39,06 Kg 36,45 Kg 35 Kg 34,01 Kg 33,26 Kg 32,66 Kg 32,16 Kg 31,73 Kg 31,36 Kg 31,03 Kg 30,74 Kg 30,47 Kg 30,23 Kg 30,00 Kg 29,80 Kg 29,61 Kg 29,43 Kg 29,26 Kg 29,10 Kg 28,95 Kg\n100% 95% 90% 85% 80% 75% 70% 65% 60% 55% 50% 45% 40% 35% 30% 25% 20% 15% 10% 5%\n39,06 Kg 37,11 Kg 35,15 Kg 33,20 Kg 31,25 Kg 29,30 Kg 27,34 Kg 25,39 Kg 23,44 Kg 21,48 Kg 19,53 Kg 17,58 Kg 15,62 Kg 13,67 Kg 11,72 Kg 9,76 Kg 7,81 Kg 5,86 Kg 3,91 Kg 1,95 Kg\nConditioning\nAMRAP 10’\n4 c2b\n6 db snatch 25/17’5\n24 du"
        return text

    def _send_keys(self, text, element, sleep_time=const.DEFAULT_ACTION_SLEEP_TIME):
        element.send_keys(text)
        self._wait(sleep_time)

    def _click(self, element, sleep_time=const.DEFAULT_ACTION_SLEEP_TIME):
        element.click()
        self._wait(sleep_time)

    def close(self):
        self.driver.quit()
