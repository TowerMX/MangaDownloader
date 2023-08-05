from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from . import const, utils
import platform
import time


class MyDriver:

    base_url = "https://mangadex.org/"

    def __init__(self, logger, sandbox=False):
        self.logger = logger
        self.sandbox = sandbox
        if self.sandbox:
            self.logger.debug("Modo sandbox activado")
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

        self.driver = webdriver.Chrome(driver_path, options=chrome_options)
        self.logger.debug(f"Se ha inicializado el driver con el os {platform_os}")


    def login(self, username, password):
        self.logger.info("Comenzando el login...")

        self._navigate(const.LOGIN_URL)

        self.logger.debug("Encontrando objetos...")
        username_box = self.driver.find_element(By.ID, const.LOGIN_USERNAME_BOX_ID)
        password_box = self.driver.find_element(By.ID, const.LOGIN_PASSWORD_BOX_ID)
        submit_box = self.driver.find_element(By.ID, const.LOGIN_SUBMIT_BOX_ID)

        self.logger.debug("Mandando teclas...")
        self._send_keys(username, username_box)
        self._send_keys(password, password_box)
        self._click(submit_box)

        self.logger.info("¡Éxito!")

        self.navigate_to_schedule()


    def download_manga(self, manga_name, manga_url, first_chapter, last_chapter, temp_path=const.DEFAULT_TEMP_FOLDER):
        return None

















    def navigate_to_schedule(self):
        self._navigate(const.SCHEDULE_URL)

    def get_all_wods(self):
        self.logger.info("Extrayendo todos los wods...")
        buttons = self.driver.find_elements_by_css_selector(
            const.SCHEDULE_WOD_BOX_CSS_ID
        )
        n_buttons = len(buttons)
        relative_path = utils.extract_rel_url_with_query(self.driver.current_url)
        wods = []
        for i in range(n_buttons):
            button = self.driver.find_elements_by_css_selector(
                const.SCHEDULE_WOD_BOX_CSS_ID
            )[i]
            # Make it visible
            self._make_visible(button)
            # Popup opens
            self._click(button)
            # Identify popup
            popup = self.driver.find_element(By.ID, const.WOD_POPUP_ID)
            # Extract info from text
            info = self._parse_text(popup.text)
            wods.append(info)
            # Refresh
            self._navigate(relative_path)

        return list(set(wods))

    def sign_up_for_training(self, training_schedule):
        self.logger.info("Registrándose en los días deseados...")
        current_day, current_time = utils.get_current_day_and_hour()
        # No se entrena el domingo
        try:
            del training_schedule[const.WEEK_DAYS[-1]]
        except KeyError:
            pass
        # days_index = [const.WEEK_DAYS.index(day) for day in training_schedule.keys()]
        # Se averigua cuáles de los días faltan por entrenar
        # (en caso de ser domingo se entrenan todos los días)
        if current_day == const.WEEK_DAYS[-1]:
            filtered_days = list(training_schedule.keys())
        else:
            filtered_days = [
                day
                for day in training_schedule.keys()
                if const.WEEK_DAYS.index(day) >= const.WEEK_DAYS.index(current_day)
            ]
        # En caso de que haya que entrenar hoy, verificar que la hora no se haya pasado:
        if current_day in filtered_days:
            # Si ya se ha pasado la hora:
            # Time1 > Time2
            if utils.compare_times(training_schedule[current_day], current_time):
                filtered_days.remove(current_day)
        self.logger.debug(f"Días a entrenar: {str(filtered_days)}")
        # Averiguamos el día de hoy en la página web
        if not const.SCHEDULE_URL in self.driver.current_url:
            self._navigate(const.SCHEDULE_URL)
        current_query_time = utils.extract_time_from_query(self.driver.current_url)
        shift = 0
        # En caso de que hoy sea domingo se atrasan todos los días y se salta el primero:
        if current_day == const.WEEK_DAYS[-1]:
            shift = 1
        # Se almacenará qué días (con sus horas) no se han podido clickar por estar llenos:
        missing_trains = {}
        # Se itera para todos los días en los que se quieran entrenar:
        for day in filtered_days:
            self.logger.debug(f"Iterando para el día: {day}")
            # Se calcula el indice relativo al dia de hoy
            if shift == 0:
                rel_index = const.WEEK_DAYS.index(day) - const.WEEK_DAYS.index(current_day)
            else:  # shift == 1:
                rel_index = const.WEEK_DAYS.index(day) + shift
            # Se navega para el día calculado
            self._navigate(
                f"{const.SCHEDULE_URL}?t={current_query_time + rel_index*const.SCHEDULE_TIME_BETWEEN_DAYS}"
            )
            # Se parsea el día para poder encontrar la etiqueta asociada:
            training_hour = training_schedule[day].split(":")[0]
            training_minute = training_schedule[day].split(":")[1]
            box_tag = f"h{training_hour}{training_minute}00"

            training_element = self.driver.find_element(By.CSS_SELECTOR,
                f'[data-magellan-destination="{box_tag}"]'
            )

            # La casuistica ahora es:
            #     1. Es hoy (hay WOD):
            #         a. Hay hueco para entrenar
            #         b. No hay hueco para entrenar
            #     2. Es otro dia o es OpenBox:
            #         a. Hay hueco para entrenar
            #         b. No hay hueco para entrenar

            # Escogemos los botones dentro del entrenamiento:
            buttons = training_element.find_elements_by_css_selector("button")

            # Identificamos si estamos antes Open Box:
            training_text = training_element.find_element(By.CSS_SELECTOR,
                '[class="entrenamiento"]'
            ).text
            open_box = False
            if const.SCHEDULE_OPEN_BOX_TEXT in training_text:
                open_box = True

            # Identificamos si es hoy:
            today = False
            if day == current_day:
                today = True

            # Si es open box u otro día
            if open_box or not today:
                button = buttons[0]
            else:  # Si es hoy y no es open box
                button = buttons[1]
            self.logger.debug(f"Es OpenBox: {open_box}\tes hoy: {today}")
            # Identificamos si hay hueco para entrenar:
            if not const.SCHEDULE_BUTTON_TRAINING_TEXT in button.text:
                # No hay hueco para entrenar
                missing_trains[day] = training_schedule[day]
                self.logger.debug(
                    f"No hay hueco para entrenar para el día {day} a la hora {training_schedule[day]}"
                )
            # Se comprueba que no estemos previamente registrados:
            try:
                # Busca el botón que avisa de que ya estás inscrito
                training_element.find_element(By.CSS_SELECTOR,
                    '[class="button  alert"]'
                )
                # Si llega a este punto es que ya estábamos inscritos
                self.logger.debug(
                    f"Ya se estaba inscrito en el entrenamiento del día {day} a la hora {training_schedule[day]}"
                )
            except NoSuchElementException:
                # En caso de que no se encuentre se clica
                if not self.sandbox:
                    self._click(button)
                self.logger.debug(
                    f"Se ha clicado el entrenamiento del día {day} a la hora {training_schedule[day]}"
                )

        return missing_trains




    def _navigate(self, rel_url):
        self.driver.get(self.base_url + rel_url)
        self._wait_browse_gap()

    def _wait_action_gap(self):
        time.sleep(const.DEFAULT_ACTION_SLEEP_TIME)

    def _wait_browse_gap(self):
        time.sleep(const.DEFAULT_BROWSE_SLEEP_TIME)

    def _make_visible(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        self.driver.execute_script(
            f"window.scrollBy(0, -{const.SCHEDULE_PIXELS_TO_SCROLL_UP});"
        )

    def _parse_text(self, text):
        # EXAMPLE = "Wod\nWeightlifting\nSquat snatch\nE2MO2M 10’\n1 x 2 80%\n2 x 2 85%\n2 x 2 90%\nE3MO3M 12’\n1 x 1 95%\n1 x 1 100%\n2 x RM\nSquat snatch\nMax (n) rep(s)\n1RM 2RM 3RM 4RM 5RM 6RM 7RM 8RM 9RM 10RM 11RM 12RM 13RM 14RM 15RM 16RM 17RM 18RM 19RM 20RM\n39,06 Kg 36,45 Kg 35 Kg 34,01 Kg 33,26 Kg 32,66 Kg 32,16 Kg 31,73 Kg 31,36 Kg 31,03 Kg 30,74 Kg 30,47 Kg 30,23 Kg 30,00 Kg 29,80 Kg 29,61 Kg 29,43 Kg 29,26 Kg 29,10 Kg 28,95 Kg\n100% 95% 90% 85% 80% 75% 70% 65% 60% 55% 50% 45% 40% 35% 30% 25% 20% 15% 10% 5%\n39,06 Kg 37,11 Kg 35,15 Kg 33,20 Kg 31,25 Kg 29,30 Kg 27,34 Kg 25,39 Kg 23,44 Kg 21,48 Kg 19,53 Kg 17,58 Kg 15,62 Kg 13,67 Kg 11,72 Kg 9,76 Kg 7,81 Kg 5,86 Kg 3,91 Kg 1,95 Kg\nConditioning\nAMRAP 10’\n4 c2b\n6 db snatch 25/17’5\n24 du"
        return text

    def _send_keys(self, text, element):
        element.send_keys(text)
        self._wait_action_gap()

    def _click(self, element):
        # Use execute_script() to click the button
        self.driver.execute_script("arguments[0].click();", element)
        self._wait_action_gap()

    def close(self):
        self.driver.quit()
