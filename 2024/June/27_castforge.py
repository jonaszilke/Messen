import time

from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor

exhibitor_list_link = "https://www.messe-stuttgart.de/castforge/besucher/ausstellerverzeichnis#/"
tools = Tools(RunMode.RUN)


def accept_cookies():
    input('Accept Cookies!!')


def parse_exhibitor(ex: Exhibitor):
    css_info = '#detail-modal > div > div > div:nth-child(3) > div > div.ed-detail__segment.ed-detail__segment--contacts'

    data = tools.get_information_from_css_link(css_info, throw_exception=True).splitlines()
    ex.name = data[1]

    for d in data[2:]:
        ex.sort_string(d)

    if tools.run_mode == RunMode.TESTING:
        print(str(ex))


def click_css_link(css_link: str, number: int, timeout=10):
    current_object = EC.presence_of_element_located((By.CSS_SELECTOR, css_link))
    try:
        WebDriverWait(tools.driver, timeout).until(current_object)
        elements = tools.driver.find_elements(By.CSS_SELECTOR, css_link)
        elements[number].click()
    except NoSuchElementException:
        element = tools.driver.find_elements(By.CSS_SELECTOR, css_link)[number]
        tools.driver.execute_script("arguments[0].click();", element)
        raise NoSuchElementException
    except TimeoutException:
        raise TimeoutException
    except ElementNotInteractableException:
        # just for clearance
        raise ElementNotInteractableException

def scroll_into_view(css_link: str, number):
    elements = tools.driver.find_elements(By.CSS_SELECTOR, css_link)
    element = elements[number]
    tools.driver.execute_script("arguments[0].scrollIntoView();", element)


if __name__ == "__main__":
    tools.open_link(exhibitor_list_link)
    tools.driver.maximize_window()
    accept_cookies()
    # tools.scroll()
    tools.driver.execute_script("window.scrollTo(0, 0);")
    second = False
    i = 62
    j = 0
    while True:

        exhibitor: Exhibitor = Exhibitor()
        try:
            css_link = f'#ed-list > div.ed-characterGroupWrapper > div.ed-characterGroup.clr > div:nth-child({i}) > div > div > a'
            if second:
                css_link = f'#ed-list > div.ed-characterGroupWrapper > div:nth-child(7) > div:nth-child({i}) > div > div > a'
            scroll_into_view(css_link, j)
            time.sleep(1)
            tools.driver.execute_script("window.scrollBy(0, -100);")
            time.sleep(1)
            click_css_link(css_link, j)
            parse_exhibitor(exhibitor)
            tools.back()
        except (TimeoutException, NoSuchElementException):
            tools.log_error(f'{i}: {exhibitor.name}')
            print(f'{i}: {exhibitor.name} !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        finally:
            tools.save_exhibitor(exhibitor)

        if i == 62:
            second = True
            i = 2
            j = 1
        else:
            i += 1


