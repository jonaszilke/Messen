import inspect
import json
import os
import re
import time
import sys
from datetime import datetime
from enum import Enum

from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException
from selenium.webdriver import Chrome, Edge, Firefox
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from tqdm import tqdm

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
        self.name = self._get_initial_script_name()
        self.data_file_path = fr'data\{self.get_file_name()}.txt'
        self.init_file(self.data_file_path)
        self.link_file_path = fr'data\{self.name}_exhibitor_links.txt'
        self.log_file_path = fr'data\{self.name}_error_log.txt'
        self.cookie_path = fr'data\{self.name}_cookies.json'
        self.local_storage_path = fr'data\{self.name}_local_storage.json'
        self.timeout = 10

    def __del__(self):
        self.driver.quit()

    def get_file_name(self):
        time_string = datetime.now().strftime('%Y%m%d_%H%M')
        file_name = self.name if self.run_mode != RunMode.RUN else f'{self.name}_full_{time_string}'
        return file_name

    def init_file(self, path):
        if not os.path.exists('data'):
            os.makedirs('data')
        with open(path, 'w', encoding='utf-8') as file:
            file.write('Name\tStraße\tPLZ\tOrt\tLand\tTelefon\tFax\tE-Mail\tUrl\tInfo\n')

    @staticmethod
    def _get_initial_script_name():
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
        current_object = EC.element_to_be_clickable((By.CSS_SELECTOR, css_link))
        try:
            WebDriverWait(self.driver, timeout).until(current_object)
            self.driver.find_element(By.CSS_SELECTOR, css_link).click()
        except NoSuchElementException:
            element = self.driver.find_element(By.CSS_SELECTOR, css_link)
            self.driver.execute_script("arguments[0].click();", element)
            raise NoSuchElementException
        except TimeoutException:
            raise TimeoutException
        except ElementNotInteractableException:
            # just for clearance
            raise ElementNotInteractableException

    def click_xpath(self, xpath: str, timeout=None):
        timeout: int = timeout if timeout is not None else self.timeout
        current_object = EC.element_to_be_clickable((By.XPATH, xpath))
        try:
            WebDriverWait(self.driver, timeout).until(current_object)
            self.driver.find_element(By.XPATH, xpath).click()
        except NoSuchElementException:
            element = self.driver.find_element(By.XPATH, xpath)
            self.driver.execute_script("arguments[0].click();", element)
            raise NoSuchElementException
        except TimeoutException:
            raise TimeoutException
        except ElementNotInteractableException:
            # just for clearance
            raise ElementNotInteractableException

    def open_in_new_tab_css_link(self, css_link: str, timeout=None):

        element = self.driver.find_element(By.CSS_SELECTOR, css_link)
        self.open_in_new_tab_element(element, timeout)

    def open_in_new_tab_element(self, element, timeout=None):
        timeout: int = timeout if timeout is not None else self.timeout
        WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(element))

        actions = ActionChains(self.driver)
        actions.move_to_element(element).key_down(Keys.CONTROL).click(element).key_up(Keys.CONTROL).perform()

        WebDriverWait(self.driver, timeout).until(
            lambda d: len(d.window_handles) > 1
        )
        self.switch_tab()

    def switch_tab(self, tab_number=-1):
        window_handles = self.driver.window_handles
        self.driver.switch_to.window(window_handles[tab_number])

    def close_tab(self):
        self.driver.close()

    def get_information_from_css_link(self, css_link, throw_exception=False, timeout=None) -> str:
        return self.get_information(By.CSS_SELECTOR, css_link, throw_exception, timeout)

    def get_information_from_xpath(self, xpath, throw_exception=False, timeout=None) -> str:
        return self.get_information(By.XPATH, xpath, throw_exception, timeout)

    def get_information(self, selector: str, link, throw_exception=False, timeout=None) -> str:
        if link == "":
            return ''
        try:
            element = self.find_element(selector, link, timeout)
            return element.text
        except (TimeoutException, NoSuchElementException) as e:
            if throw_exception:
                raise e
            else:
                return ''

    def get_href_from_css_link(self, css_link, throw_exception=False, timeout=None) -> str:
        return self.get_href(By.CSS_SELECTOR, css_link, throw_exception, timeout)

    def get_href_from_xpath(self, xpath, throw_exception=False, timeout=None) -> str:
        return self.get_href(By.XPATH, xpath, throw_exception, timeout)

    def get_href(self, selector: str, link, throw_exception=False, timeout=None) -> str:
        if link == "":
            return ''
        try:
            element = self.find_element(selector, link, timeout)
            return element.get_attribute("href")
        except (TimeoutException, NoSuchElementException) as e:
            if throw_exception:
                raise e
            else:
                return ''

    def find_element(self, selector: str, link, timeout=None) -> WebElement:
        timeout: int = timeout if timeout is not None else self.timeout
        strategies = [getattr(By, attr) for attr in dir(By) if not attr.startswith("__")]
        if selector not in strategies:
            raise ValueError(f"Invalid selector: '{selector}'. Must be one the selectors defined in the By class.")
        try:
            element_present = EC.presence_of_element_located((selector, link))
            WebDriverWait(self.driver, timeout).until(element_present)
            return self.driver.find_element(By.CSS_SELECTOR, link)
        except (TimeoutException, NoSuchElementException) as e:
            raise e

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

    def save_exhibitor(self, exhibitor: Exhibitor, print_name=True):
        if self.run_mode == RunMode.TESTING:
            print(str(exhibitor))
        elif print_name:
            print(exhibitor.name)

        if exhibitor.name != '':
            with open(self.data_file_path, 'a', encoding='utf-8') as file:
                file.write(str(exhibitor))

    def log_error(self, message: str):
        with open(self.log_file_path, 'a', encoding='utf-8') as f:
            f.write(message + '\n')

    def remove_old_log_file(self):
        if os.path.exists(self.log_file_path):
            os.remove(self.log_file_path)

    def back(self):
        self.driver.back()

    def get_saved_links(self):
        if os.path.exists(self.link_file_path):
            with open(self.link_file_path, 'r') as file:
                links = [link.replace('\n', '') for link in file.readlines() if link != '\n']
                links = list(set(links))
                return links
        return []

    def save_links(self, links, path=None):
        path = self.link_file_path if path is None else path
        with open(path, 'w', encoding="utf-8") as file:
            links = list(set(links))
            file.write('\n'.join(links))

    def wait_for_element(self, css_link: str, timeout=None):
        timeout: int = timeout if timeout is not None else self.timeout
        try:
            WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, css_link)))
        except TimeoutException:
            return False
        return True

    def reload_driver(self):
        self.driver.quit()
        self.driver = WebDriverFactory.create_driver(browser_type)

    def scroll_css_into_view(self, css_link: str, sleep_time=1):
        element = self.driver.find_element(By.CSS_SELECTOR, css_link)
        self.scroll_element_into_view(element, sleep_time=sleep_time)

    def scroll_element_into_view(self, element: WebElement, sleep_time=1):
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        time.sleep(sleep_time)
        self.driver.execute_script("window.scrollBy(0, -300);")
        time.sleep(1)

    def get_elements_by_css(self, css_link):
        return self.driver.find_elements(By.CSS_SELECTOR, css_link)

    def get_links(self, function, use_save_links=True):
        links = self.get_saved_links() if use_save_links else []
        if len(links) != 0:
            return links

        links = function()
        links_no_dupes = []
        [links_no_dupes.append(i) for i in links if
         not links_no_dupes.count(i)]  # remove duplicates while keeping the order

        self.save_links(links_no_dupes)
        return links_no_dupes

    def iterate_exhibitor_links(self, links: list[str], parse_exhibitor):
        start_time = time.time()
        print(f'Parse {len(links)} exhibitors')
        with tqdm(total=len(links), position=0, leave=True, file=sys.stdout,
                  bar_format='{desc:<30}{percentage:1.0f}%|{bar:40}{r_bar}') as pbar:
            for link in links:
                exhibitor: Exhibitor = Exhibitor()
                try:
                    self.open_link(link)
                    parse_exhibitor(exhibitor)
                except Exception:
                    self.log_error(link)
                finally:
                    self.save_exhibitor(exhibitor, print_name=False)
                    new_desc = exhibitor.name + (50 * ' ')
                    pbar.set_description(new_desc[:50])
                    pbar.update(1)

        end_time = time.time()
        elapsed_time = end_time - start_time
        hours, rem = divmod(elapsed_time, 3600)
        minutes, seconds = divmod(rem, 60)
        print(f"Time taken: {int(hours)} hours, {int(minutes)} minutes, and {seconds:.2f} seconds")

    def save_local_storage(self):
        local_storage = self.driver.execute_script("return {...localStorage};")
        with open(self.local_storage_path, 'w') as file:
            json.dump(local_storage, file)

    def load_local_storage(self):
        if not os.path.exists(self.local_storage_path):
            return False

        with open(self.local_storage_path, "r") as file:
            local_storage = json.load(file)
        for key, value in local_storage.items():
            self.driver.execute_script(f"localStorage.setItem('{key}', '{value}');")
        return True



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
