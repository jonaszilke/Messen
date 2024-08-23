import time

from selenium.common.exceptions import TimeoutException

from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor
from selenium.webdriver.common.by import By

exhibitor_list_link = "https://www.ausstellungs-gmbh.de/ostbayernschau/fuer-besucher/ausstellerverzeichnis-2024/"
tools = Tools(RunMode.RUN)


def accept_cookies():
    css_accept = '#BorlabsCookieBox > div > div > div > div.cookie-box > div > div > div > p:nth-child(4) > a'
    tools.click_css_link(css_accept)


def parse_exhibitor(ex: Exhibitor, data: list[str]):
    ex.name = data[0]

    new_data = []

    for d in data[1:]:
        new_d = d.replace('Tel.', '').strip()
        if ' · ' in new_d:
            new_data += new_d.split(' · ')
        else:
            new_data.append(new_d)

    for d in new_data:
        ex.sort_string(d)

    css_web = 'div.category_rows > div.fair_row_master.exhibitor.active > div > div.fair_row_extended.toggled > a'
    web = tools.get_information_from_css_link(css_web, timeout=0.2)
    ex.sort_string(web)


    if tools.run_mode == RunMode.TESTING:
        print(str(ex))

def get_all_elements(css_link: str):
    elements = tools.driver.find_elements(By.CSS_SELECTOR, css_link)
    return elements

if __name__ == "__main__":
    tools.open_link(exhibitor_list_link)
    tools.driver.maximize_window()
    time.sleep(2)
    accept_cookies()
    time.sleep(2)
    css_link = 'div.fair_row_plus'
    elements_plus = get_all_elements(css_link)
    css_text = 'div.exhibitor_row_extended'
    elements_text = get_all_elements(css_text)
    i = 1
    for (index, e) in enumerate(elements_plus):
        exhibitor: Exhibitor = Exhibitor()
        try:
            e.click()
            text = elements_text[index].text
            parse_exhibitor(exhibitor, text.splitlines())
        except TimeoutException:
            tools.log_error(str(i))
        finally:
            tools.save_exhibitor(exhibitor)
        i += 1
