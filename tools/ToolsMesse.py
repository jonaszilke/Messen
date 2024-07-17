from selenium.common.exceptions import TimeoutException, ElementNotInteractableException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
import time
from bs4 import BeautifulSoup
import re
import inspect
import os
from enum import Enum

class RunMode(Enum):
    TESTING = 0
    DEBUG = 1
    RUN = 2


class Tools:
    def __init__(self, run_mode=RunMode.TESTING):
        self.run_mode = run_mode
        self.driver = Chrome()
        self.name = self.get_initial_script_name()
        self.file = self.init_file()
        self.timeout = 5

    def __del__(self):
        self.driver.quit()
        self.file.close()

    def init_file(self):
        file_name = self.name if self.run_mode != RunMode.RUN else f'{self.name}_full_{time.time()}'
        file = open(f'{file_name}.txt', 'w', encoding='utf-8')
        file.write('Name\tStraße\tPLZ\tOrt\tLand\tTelefon\tFax\tE-Mail\tUrl\tInfo\n')
        return file

    def get_initial_script_name(self):
        stack = inspect.stack()
        for frame_info in reversed(stack):
            if frame_info.function == '<module>':
                return os.path.basename(frame_info.filename)[:-3]
        return None

    def open_link(self, link):
        self.driver.get(link)

    def click_css_link(self, css_link: str, timeout=None):
        timeout: int = timeout if timeout is not None else self.timeout
        current_object = EC.presence_of_element_located((By.CSS_SELECTOR, css_link))
        WebDriverWait(self.driver, timeout).until(current_object)
        try:
            self.driver.find_element(By.CSS_SELECTOR, css_link).click()
        except NoSuchElementException:
            element = self.driver.find_element(By.CSS_SELECTOR, css_link)
            self.driver.execute_script("arguments[0].click();", element)
        except ElementNotInteractableException:
            # just for clearance
            raise ElementNotInteractableException

    def get_information_from_css_link(self, css_link, throw_exception=False, timeout=None):
        timeout: int = timeout if timeout is not None else self.timeout
        try:
            element_present = EC.presence_of_element_located((By.CSS_SELECTOR, css_link))
            WebDriverWait(self.driver, timeout).until(element_present)
            return self.driver.find_element(By.CSS_SELECTOR, css_link).text
        except TimeoutException as e:
            if throw_exception:
                print(e)
                raise e
            else:
                print("TIMEOUT")
        except NoSuchElementException as e:
            if throw_exception:
                raise e
            else:
                print("NO_SUCH_ELEMENT")
        return ""

    def get_href_from_css_link(self, css_link, throw_exception=False):
        try:
            element_present = EC.presence_of_element_located((By.CSS_SELECTOR, css_link))
            WebDriverWait(self.driver, self.timeout).until(element_present)
            return self.driver.find_element(By.CSS_SELECTOR, css_link).get_attribute("href")
        except TimeoutException as e:
            if throw_exception:
                raise e
            else:
                print("TIMEOUT")
        except NoSuchElementException as e:
            print("NO_SUCH_ELEMENT")
        return ""

    def scroll(self):
        lenOfPage = self.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        match = False
        while not match:
            lastCount = lenOfPage
            time.sleep(3)
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
