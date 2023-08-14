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
import base64
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
        initial_url = self.driver.current_url
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
                if remember_me is True:
                    self._click(remember_me_box)
                self._click(submit_box)

                current_url = self.driver.current_url
                while current_url != initial_url:
                    self._wait(const.DEFAULT_LOGIN_SLEEP_TIME)
                    current_url = self.driver.current_url
                self.logger.info("Se ha iniciado sesión correctamente.")
            except Exception:
                self.logger.error("No se ha podido iniciar sesión.")
        except NoSuchElementException:
            # En caso de que no se encuentre el botón de registrarse, la sesión estaba iniciada
            self.logger.info("La sesión ya estaba iniciada.")


    def download_manga(self, manga_name, manga_url, first_chapter="first", last_chapter="last", trim_first_pages=0, trim_last_pages=0, temp_folder=const.DEFAULT_TEMP_FOLDER):
        self.logger.info(f"Comenzando descarga de imágenes de {manga_name}...")
        # Crea carpeta del manga
        try:
            Path(rf"{temp_folder}\{manga_name}").mkdir(exist_ok=True)
        except NotADirectoryError:
            self.logger.error(f"El nombre {manga_name} no es válido.")
            return False

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
            except (ValueError, IndexError, Exception):
                self._wait(const.DEFAULT_RETRY_SLEEP_TIME)

        if volume == "Oneshot":
            pass
        elif isinstance(first_chapter, int) or isinstance(first_chapter, float):
            previous_chapter = current_chapter + 1
            while not current_chapter == first_chapter:
                if current_chapter == previous_chapter:
                    self.logger.warning(f"Se ha introducido un número de primer capítulo ({first_chapter}) inferior al primero disponible ({current_chapter}). Se ha descargado a partir de dicho capítulo.")
                    break
                if current_chapter < first_chapter:
                    self._change_chapter(direction="forward")
                else:
                    self._change_chapter(direction="backward")
                previous_chapter = current_chapter
                status_updated = False
                while not status_updated:
                    try:
                        current_chapter = float(self._get_page_status()[1])
                        status_updated = True
                    except (ValueError, IndexError, Exception):
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
                    except (ValueError, IndexError, Exception):
                        self._wait(const.DEFAULT_RETRY_SLEEP_TIME)
        else:
            self.logger.error("Parámetro first_chapter de mangalist.yaml no reconocido.")
            return False

        status_updated = False
        while not status_updated:
            try:
                initial_page = int(self._get_page_status()[2])
                status_updated = True
            except (ValueError, IndexError, Exception):
                self._wait(const.DEFAULT_RETRY_SLEEP_TIME)
        while initial_page > 1:
            self._turn_page(direction="backward")
            status_updated = False
            while not status_updated:
                try:
                    initial_page = int(self._get_page_status()[2])
                    status_updated = True
                except (ValueError, IndexError, Exception):
                    self._wait(const.DEFAULT_RETRY_SLEEP_TIME)

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

            current_chapter, is_last_page = self._download_image(manga_name, trim_first_pages=trim_first_pages, trim_last_pages=trim_last_pages, temp_folder=temp_folder)

            if is_last_page:
                self._turn_page(direction="forward", sleep_time=const.DEFAULT_CHAPTER_CHANGE_SLEEP_TIME)
                current_chapter += 0.0001
            else:
                self._turn_page(direction="forward")

        self.logger.info(f"Manga {manga_name} descargado correctamente.")
        return True


    def _download_image(self, manga_name, trim_first_pages=0, trim_last_pages=0, temp_folder=const.DEFAULT_TEMP_FOLDER):
        status_updated = False
        while not status_updated:
            try:
                volume, chapter, page, last_page = self._get_page_status()
                image_element = self.driver.find_element(By.XPATH, const.MANGA_IMAGE_XPATH)
                status_updated = True
            except (NoSuchElementException, ValueError, IndexError, Exception):
                self._wait(const.DEFAULT_RETRY_SLEEP_TIME)

        if trim_first_pages + trim_last_pages >= int(last_page):
            self.logger.error(f"El número de páginas a recortar ({trim_first_pages + trim_last_pages}) es superior o igual al número de páginas del capítulo ({last_page}).")
            return float(chapter), page == last_page
        if int(page) <= trim_first_pages or int(last_page) - int(page) < trim_last_pages:
            self.logger.info(f"Página a recortar, no se descarga.")
            return float(chapter), page == last_page

        if volume == "Oneshot":
            self.logger.info(f"Oneshot, Pages: {page} / {last_page}")
        elif volume == "No volumes":
            self.logger.info(f"Ch. {chapter}, Pages: {page} / {last_page}")
        else:
            self.logger.info(f"Vol. {volume}, Ch. {chapter}, Pages: {page} / {last_page}")

        if volume == "Oneshot":
            volume_folder = "Oneshot"
            chapter_folder = ""
        elif volume == "No volumes":
            volume_folder = "No volumes"
            chapter_folder = f"{const.CHAPTER_PREFIX} {chapter}"
        else:
            volume_folder = f"{const.VOLUME_PREFIX} {volume}"
            chapter_folder = f"{const.CHAPTER_PREFIX} {chapter}"

        image_extension = image_element.get_attribute("alt").split(".")[-1]

        # Crea carpeta del volumen
        Path(rf"{temp_folder}\{manga_name}\{volume_folder}").mkdir(exist_ok=True)

        if volume == "Oneshot":
            image_path = rf"{temp_folder}\{manga_name}\{volume_folder}\{page}.{image_extension}"
        else:
            # Crea carpeta del capítulo
            Path(rf"{temp_folder}\{manga_name}\{volume_folder}\{chapter_folder}").mkdir(exist_ok=True)
            image_path = rf"{temp_folder}\{manga_name}\{volume_folder}\{chapter_folder}\{page}.{image_extension}"

        image_downloaded = False
        while not image_downloaded:
            try:
                image_bytes = self.get_file_content_chrome(image_element.get_attribute("src"))
                image_downloaded = True
            except Exception:
                pass

        with open(image_path, "wb") as img:
            img.write(image_bytes)

        return float(chapter), page==last_page


    def _get_page_status(self):
        chapter_element = self.driver.find_element(By.XPATH, const.MANGA_CHAPTER_XPATH)
        page_element = self.driver.find_element(By.XPATH, const.MANGA_PAGE_XPATH)
        
        if chapter_element.text == "Oneshot":
            volume = "Oneshot"
            chapter = "1"
        else:
            chapter_split = chapter_element.text.split(", ")
            if len(chapter_split) == 1:
                volume = "No volumes"
                chapter = chapter_split[0].split(" ")[1]
            else:
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
        if direction == "forward":
            self._press_key(Keys.RIGHT, sleep_time=sleep_time)
        elif direction == "backward":
            self._press_key(Keys.LEFT, sleep_time=sleep_time)
        else:
            raise ValueError(f"Direction {direction} not valid")


    def _change_chapter(self, direction="forward", sleep_time=const.DEFAULT_CHAPTER_CHANGE_SLEEP_TIME):
        if direction == "forward":
            self._press_key(".", sleep_time=sleep_time)
        elif direction == "backward":
            self._press_key(",", sleep_time=sleep_time)
        else:
            raise ValueError(f"Direction {direction} not valid")


    def _wait(self, sleep_time):
        time.sleep(sleep_time)


    def _press_key(self, key, sleep_time=const.DEFAULT_ACTION_SLEEP_TIME):
        ActionChains(self.driver).send_keys(key).perform()
        self._wait(sleep_time)


    def _send_keys(self, text, element, sleep_time=const.DEFAULT_ACTION_SLEEP_TIME):
        element.send_keys(text)
        self._wait(sleep_time)


    def _click(self, element, sleep_time=const.DEFAULT_ACTION_SLEEP_TIME):
        element.click()
        self._wait(sleep_time)


    def close(self):
        self.driver.quit()
