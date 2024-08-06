from datetime import datetime

from selenium.common.exceptions import TimeoutException, ElementNotInteractableException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome, Edge, Firefox
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
import re
import inspect
import os
from enum import Enum
from config import browser_type
from tools.exhibitor import Exhibitor


class RunMode(Enum):
    TESTING = 0
    DEBUG = 1
    RUN = 2


class Tools:
    def __init__(self, run_mode=RunMode.TESTING):
        self.run_mode = run_mode
        self.driver = WebDriverFactory.create_driver(browser_type)
        self.name = self.get_initial_script_name()
        self.file = self.init_file()
        self.timeout = 10

    def __del__(self):
        self.driver.quit()
        self.file.close()

    def init_file(self):
        if not os.path.exists('data'):
            os.makedirs('data')
        time_string = datetime.now().strftime('%Y%m%d_%H%M')
        file_name = self.name if self.run_mode != RunMode.RUN else f'{self.name}_full_{time_string}'
        file = open(fr'data\{file_name}.txt', 'w', encoding='utf-8')
        file.write('Name\tStraße\tPLZ\tOrt\tLand\tTelefon\tFax\tE-Mail\tUrl\tInfo\n')
        return file

    def get_initial_script_name(self):
        stack = inspect.stack()
        for frame_info in reversed(stack):
            if frame_info.function == '<module>':
                filename = frame_info.filename
                if 'pydev' not in filename:  # Ignore pydev-related frames when in debugging mode
                    return os.path.basename(filename)[:-3]
        return None

    def open_link(self, link):
        self.driver.get(link)

    def click_css_link(self, css_link: str, timeout=None):
        timeout: int = timeout if timeout is not None else self.timeout
        current_object = EC.presence_of_element_located((By.CSS_SELECTOR, css_link))
        try:
            WebDriverWait(self.driver, timeout).until(current_object)
            self.driver.find_element(By.CSS_SELECTOR, css_link).click()
        except NoSuchElementException:
            element = self.driver.find_element(By.CSS_SELECTOR, css_link)
            self.driver.execute_script("arguments[0].click();", element)
        except TimeoutException:
            if self.run_mode == RunMode.DEBUG:
                print("Time")
        except ElementNotInteractableException:
            # just for clearance
            raise ElementNotInteractableException

    def get_information_from_css_link(self, css_link, throw_exception=False, timeout=None):
        if css_link == "":
            return ""
        timeout: int = timeout if timeout is not None else self.timeout
        try:
            element_present = EC.presence_of_element_located((By.CSS_SELECTOR, css_link))
            WebDriverWait(self.driver, timeout).until(element_present)
            return self.driver.find_element(By.CSS_SELECTOR, css_link).text
        except TimeoutException as e:
            if throw_exception:
                if self.run_mode == RunMode.DEBUG:
                    print(e)
                raise e
            else:
                if self.run_mode == RunMode.DEBUG:
                    print("TIMEOUT")
        except NoSuchElementException as e:
            if throw_exception:
                raise e
            else:
                if self.run_mode == RunMode.DEBUG:
                    print("NO_SUCH_ELEMENT")
        return ""

    def get_href_from_css_link(self, css_link, throw_exception=False, timeout=None):
        timeout: int = timeout if timeout is not None else self.timeout
        try:
            element_present = EC.presence_of_element_located((By.CSS_SELECTOR, css_link))
            WebDriverWait(self.driver, timeout).until(element_present)
            return self.driver.find_element(By.CSS_SELECTOR, css_link).get_attribute("href")
        except TimeoutException as e:
            if throw_exception:
                raise e
            else:
                if self.run_mode == RunMode.DEBUG:
                    print("TIMEOUT")
        except NoSuchElementException as e:
            if self.run_mode == RunMode.DEBUG:
                print("NO_SUCH_ELEMENT")
        return ""

    def scroll(self, timeout=3):
        lenOfPage = self.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        match = False
        while not match:
            lastCount = lenOfPage
            time.sleep(timeout)
            lenOfPage = self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            if lastCount == lenOfPage:
                match = True

    def find_links(self, filter_str=''):
        links = []
        source_data = self.driver.page_source
        soup = BeautifulSoup(source_data, "lxml")

        for a in soup.find_all("a", href=re.compile(filter_str)):
            links.append(a['href'])
        return list(dict.fromkeys(links))

    def save_exhibitor(self, exhibitor: Exhibitor):
        self.file.write(str(exhibitor))
        print(exhibitor.name)

    def log_error(self, message: str):
        with open('data/' + self.name + '_error_log.txt', 'a', encoding='utf-8') as f:
            f.write(message + '\n')

    def remove_old_log_file(self):
        file_path = 'data/' + self.name + '_error_log.txt'
        if os.path.exists(file_path):
            os.remove(file_path)

    def back(self):
        self.driver.back()

class WebDriverFactory:
    @staticmethod
    def create_driver(driver_type: str):
        if driver_type.lower() == 'chrome':
            chrome_options = Options()
            chrome_options.add_argument("--disable-search-engine-choice-screen")
            return Chrome(options=chrome_options)
        elif driver_type.lower() == 'firefox':
            return Firefox()
        elif driver_type.lower() == 'edge':
            return Edge()
