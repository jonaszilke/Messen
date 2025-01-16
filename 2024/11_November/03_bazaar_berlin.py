import time
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException, NoSuchElementException, \
    ElementClickInterceptedException

from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor

exhibitor_list_link = "https://www.bazaar-berlin.de/de/die-messe/ausstellerverzeichnis/#/suche/f=h-entity_orga;v_sg=0;v_fg=0;v_fpa=FUTURE"
tools = Tools(RunMode.RUN)


def accept_cookies():
    input('Accept Cookies')

def open_all_exhibitors():
    if tools.run_mode == RunMode.RUN:
        while True:
            tools.scroll()
            show_more_css = '#onlineGuide > div > div.EWP5KKC-e-I > div:nth-child(1) > div:nth-child(2) > div.EWP5KKC-u-b > div.EWP5KKC-u-c'
            try:
                tools.click_css_link(show_more_css)
            except (ElementNotInteractableException, ElementClickInterceptedException, TimeoutException):
                break
    else:
        tools.scroll()
    tools.driver.execute_script("window.scrollTo(0, 0);")


def parse_exhibitor(ex: Exhibitor):
    css_name = '[itemprop="legalName"]'
    css_street = '[itemprop="streetAddress"]'
    css_postcode = '[itemprop="postalCode"]'
    css_city = '[itemprop="addressLocality"]'
    css_country = '[itemprop="addressCountry"]'
    css_url = '[itemprop="url"]'
    css_info = '#onlineGuidePopup > div > div > div:nth-child(1) > div.EWP5KKC-y-r > div:nth-child(2) > div > div.EWP5KKC-y-Jb > div.EWP5KKC-y-Fb > div > div.gwt-HTML'
    css_tel = '[itemprop="telephone"]'
    css_mail = 'a.gwt-Anchor.EWP5KKC-y-C'
    css_fax = '[itemprop="faxNumber"]'

    ex.name = tools.get_information_from_css_link(css_name, throw_exception=True)
    ex.url = tools.get_information_from_css_link(css_url, timeout=0.5, throw_exception=False)
    ex.tel = tools.get_information_from_css_link(css_tel, timeout=0.5, throw_exception=False)
    ex.fax = tools.get_information_from_css_link(css_fax, timeout=0.5, throw_exception=False)

    ex.street = tools.get_information_from_css_link(css_street, timeout=0.5, throw_exception=False)
    ex.postcode = tools.get_information_from_css_link(css_postcode, timeout=0.5, throw_exception=False)
    ex.city = tools.get_information_from_css_link(css_city, timeout=0.5, throw_exception=False)
    ex.country = tools.get_information_from_css_link(css_country, timeout=0.5, throw_exception=False)

    info = tools.get_information_from_css_link(css_info, timeout=0.5, throw_exception=False)
    ex.add_info(info)

    elements = tools.get_elements_by_css(css_mail)
    for elem in elements:
        ex.sort_string(elem.text)



if __name__ == "__main__":
    tools.open_link(exhibitor_list_link)
    tools.driver.maximize_window()

    time.sleep(2)

    accept_cookies()
    time.sleep(2)
    open_all_exhibitors()
    counter = 0
    for i in range(1,30):
        j = 1 # run index
        while True:
            exhibitor: Exhibitor = Exhibitor()
            css_link = f'#onlineGuide > div > div.EWP5KKC-e-I > div:nth-child(1) > div:nth-child(2) > div.listContentContainer > div:nth-child({i}) > div.EWP5KKC-e-J > div:nth-child({j}) > div.EWP5KKC-w-l > div.EWP5KKC-w-w > div.EWP5KKC-d-h > div.gwt-Label.EWP5KKC-w-Q'
            try:
                tools.click_css_link(css_link)
            except TimeoutException:
                tools.log_error(f"LAST EXHIBITOR FOR LETTER {i}: {j}")
                break
            try:
                parse_exhibitor(exhibitor)
                tools.back()
            except Exception:
                tools.log_error(f"{i}/{j}: " + exhibitor.name)
            finally:
                tools.save_exhibitor(exhibitor)

            j += 1
