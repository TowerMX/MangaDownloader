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
from PIL import Image
import base64
import io
from . import const


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
        # Abre el menú de usuario
        avatar = self.driver.find_element(By.ID, const.AVATAR_ID)
        self._click(avatar)

        try:
            # Busca el botón de registrarse
            self.driver.find_element(By.XPATH, const.REGISTER_BUTTON_XPATH)

            # Si llega a este punto es que la sesión no está iniciada
            self.logger.info("Comenzando el login...")

            try:
                signin_button = self.driver.find_element(By.XPATH, const.SIGN_IN_BUTTON_XPATH)
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
            except Exception:
                self.logger.error("No se ha podido iniciar sesión.")
        except NoSuchElementException:
            # En caso de que no se encuentre el botón de registrarse, la sesión estaba iniciada
            self.logger.info("La sesión ya estaba iniciada.")


    def download_manga(self, manga_name, manga_url, first_chapter="first", last_chapter="last", temp_folder=const.DEFAULT_TEMP_FOLDER):
        self.logger.info(f"Comenzando descarga de imágenes de {manga_name}...")
        manga_path = Path(rf"{temp_folder}\{manga_name}")
        manga_path.mkdir(exist_ok=True)

        manga_url_split = manga_url.split("/")
        url_check = manga_url_split[3] if len(manga_url_split) >= 4 else None

        if url_check == "chapter":
            self._navigate(manga_url)
        elif url_check == "title":
            self.logger.warning("Esta es la URL de un manga, pero se debe introducir la URL de una página una vez dentro. El manga no se descargará.")
            return False
        else:
            self.logger.error("Error en la URL, el manga no se descargará.")
            return False

        volume = None
        current_chapter = None
        status_updated = False
        while not status_updated:
            try:
                volume, current_chapter = self._get_page_status()[0], float(self._get_page_status()[1])
                status_updated = True
            except (ValueError, IndexError):
                self._wait(const.DEFAULT_RETRY_SLEEP_TIME)

        if volume == "Oneshot":
            pass
        elif isinstance(first_chapter, int) or isinstance(first_chapter, float):
            while not current_chapter == first_chapter:
                if current_chapter < first_chapter:
                    self._change_chapter(direction="forward")
                else:
                    self._change_chapter(direction="backward")
                status_updated = False
                while not status_updated:
                    try:
                        current_chapter = float(self._get_page_status()[1])
                        status_updated = True
                    except (ValueError, IndexError):
                        self._wait(const.DEFAULT_RETRY_SLEEP_TIME)
        elif first_chapter == "first":
            previous_chapter = current_chapter + 1
            while not current_chapter == previous_chapter:
                self._change_chapter(direction="backward")
                previous_chapter = current_chapter
                status_updated = False
                while not status_updated:
                    try:
                        current_chapter = float(self._get_page_status()[1])
                        status_updated = True
                    except (ValueError, IndexError):
                        self._wait(const.DEFAULT_RETRY_SLEEP_TIME)
        else:
            self.logger.error("Parámetro first_chapter de mangalist.yaml no reconocido.")
            return False

        status_updated = False
        while not status_updated:
            try:
                initial_page = int(self._get_page_status()[2])
                status_updated = True
            except (ValueError, IndexError):
                self._wait(const.DEFAULT_RETRY_SLEEP_TIME)
        while initial_page > 1:
            self._turn_page(direction="backward")
            status_updated = False
            while not status_updated:
                try:
                    initial_page = int(self._get_page_status()[2])
                    status_updated = True
                except (ValueError, IndexError):
                    self._wait(const.DEFAULT_RETRY_SLEEP_TIME)

        is_last_page = False

        if not (isinstance(last_chapter, int) or isinstance(last_chapter, float) or last_chapter == "last"):
            self.logger.error("Parámetro last_chapter de mangalist.yaml no reconocido.")
            return False

        # Volume/Chapter/Page loop
        while last_chapter == "last" or current_chapter <= last_chapter:
            current_url = self.driver.current_url
            url_check = current_url.split("/")[3]

            if url_check == "chapter":
                pass
            elif url_check == "title":
                if last_chapter != "last":
                    current_chapter_split = str(round(current_chapter,3)).split(".")
                    if len(current_chapter_split) == 2 and current_chapter_split[1] == "0":
                        parsed_current_chapter = current_chapter_split[0]
                    else:
                        parsed_current_chapter = str(round(current_chapter,3))
                    self.logger.warning(f"Se ha introducido un número de último capítulo ({last_chapter}) superior al último disponible ({parsed_current_chapter}). Se ha descargado hasta dicho capítulo.")
                break
            else:
                self.logger.error("Error en la URL durante la descarga. Descarga del manga incompleta.")
                return False

            page_downloaded = False
            while not page_downloaded:
                try:
                    image_element = self.driver.find_element(By.XPATH, const.MANGA_IMAGE_XPATH)
                    is_last_page, current_chapter = self._download_image(image_element, manga_name, temp_folder)
                    page_downloaded = True
                except NoSuchElementException:
                    pass

            if is_last_page:
                self._turn_page(direction="forward", sleep_time=const.DEFAULT_CHAPTER_CHANGE_SLEEP_TIME)
                current_chapter += 0.0001
            else:
                self._turn_page(direction="forward")

        self.logger.info(f"Manga {manga_name} descargado correctamente.")
        return True


    def _download_image(self, image_element, manga_name, temp_folder=const.DEFAULT_TEMP_FOLDER):
        status_updated = False
        while not status_updated:
            try:
                volume, chapter, page, last_page = self._get_page_status()
                if volume == "Oneshot":
                    self.logger.info(f"Vol. {volume}, Ch. {chapter}, Pages: {page} / {last_page}")
                else:
                    self.logger.info(f"Oneshot, Pages: {page} / {last_page}")
                status_updated = True
            except (ValueError, IndexError):
                self._wait(const.DEFAULT_RETRY_SLEEP_TIME)

        if volume == "Oneshot":
            volume_folder = "Oneshot"
            chapter_folder = ""
        else:
            volume_folder = f"{const.VOLUME_FOLDER_STRING} {volume}"
            chapter_folder = f"{const.CHAPTER_FOLDER_STRING} {chapter}"

        image_extension = image_element.get_attribute("alt").split(".")[-1]
        # image_extension = "png"
        volume_path = Path(rf"{temp_folder}\{manga_name}\{volume_folder}")
        volume_path.mkdir(exist_ok=True)

        if volume == "Oneshot":
            image_path = rf"{temp_folder}\{manga_name}\{volume_folder}\{page}.{image_extension}"
        else:
            chapter_path = Path(rf"{temp_folder}\{manga_name}\{volume_folder}\{chapter_folder}")
            chapter_path.mkdir(exist_ok=True)
            image_path = rf"{temp_folder}\{manga_name}\{volume_folder}\{chapter_folder}\{page}.{image_extension}"

        image_downloaded = False
        while not image_downloaded:
            try:
                image_bytes = self.get_file_content_chrome(image_element.get_attribute("src"))
                image_downloaded = True
            except Exception:
                pass
        image = Image.open(io.BytesIO(base64.decodebytes(image_bytes)))
        image.save(image_path)
        '''
        with open(image_path, "wb") as img:
            img.write(base64.decodebytes(image_bytes))
        '''

        '''
        # Assuming base64_str is the string value without 'data:image/jpeg;base64,'
        img = Image.open(io.BytesIO(base64.decodebytes(bytes(image_bytes, "utf-8"))))
        img.save("my-image.jpeg")
        '''

        is_last_page = page == last_page
        return is_last_page, float(chapter)


    def _get_page_status(self):
        chapter_element = self.driver.find_element(By.XPATH, const.MANGA_CHAPTER_XPATH)
        page_element = self.driver.find_element(By.XPATH, const.MANGA_PAGE_XPATH)

        if chapter_element.text == "Oneshot":
            volume = "Oneshot"
            chapter = "1"
        else:
            chapter_split = chapter_element.text.split(", ")
            volume = chapter_split[0].split(" ")[1]
            chapter = chapter_split[1].split(" ")[1]

        page_split = page_element.text.split(" / ")
        page = page_split[0].split(" ")[1]
        last_page = page_split[1]

        return volume, chapter, page, last_page


    def get_file_content_chrome(self, uri):
        result = self.driver.execute_async_script(
            """
        var uri = arguments[0];
        var callback = arguments[1];
        var toBase64 = function(buffer){for(var r,n=new Uint8Array(buffer),t=n.length,a=new Uint8Array(4*Math.ceil(t/3)),i=new Uint8Array(64),o=0,c=0;64>c;++c)i[c]="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".charCodeAt(c);for(c=0;t-t%3>c;c+=3,o+=4)r=n[c]<<16|n[c+1]<<8|n[c+2],a[o]=i[r>>18],a[o+1]=i[r>>12&63],a[o+2]=i[r>>6&63],a[o+3]=i[63&r];return t%3===1?(r=n[t-1],a[o]=i[r>>2],a[o+1]=i[r<<4&63],a[o+2]=61,a[o+3]=61):t%3===2&&(r=(n[t-2]<<8)+n[t-1],a[o]=i[r>>10],a[o+1]=i[r>>4&63],a[o+2]=i[r<<2&63],a[o+3]=61),new TextDecoder("ascii").decode(a)};
        var xhr = new XMLHttpRequest();
        xhr.responseType = 'arraybuffer';
        xhr.onload = function(){ callback(toBase64(xhr.response)) };
        xhr.onerror = function(){ callback(xhr.status) };
        xhr.open('GET', uri);
        xhr.send();
        """,
            uri,
        )
        if type(result) == int:
            raise Exception("Request failed with status %s" % result)
        return base64.b64decode(result)


    def navigate_to_home(self):
        self._navigate(const.HOME_URL)


    def _navigate(self, url, sleep_time=const.DEFAULT_BROWSE_SLEEP_TIME):
        self.driver.get(url)
        self._wait(sleep_time)


    def _turn_page(self, direction="forward", sleep_time=const.DEFAULT_PAGE_TURN_SLEEP_TIME):
        actions = ActionChains(self.driver)
        if direction == "forward":
            actions.send_keys(Keys.RIGHT)
        elif direction == "backward":
            actions.send_keys(Keys.LEFT)
        else:
            raise ValueError(f"Direction {direction} not valid")
        actions.perform()
        self._wait(sleep_time)


    def _change_chapter(self, direction="forward", sleep_time=const.DEFAULT_CHAPTER_CHANGE_SLEEP_TIME):
        actions = ActionChains(self.driver)
        if direction == "forward":
            actions.send_keys(".")
        elif direction == "backward":
            actions.send_keys(",")
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
