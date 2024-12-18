import time
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException, NoSuchElementException, \
    ElementClickInterceptedException

from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor

exhibitor_list_link = "https://www.consumenta.de/ausstellerverzeichnis/#/suche/f=h-entity_orga,h-cat_mainEventOrgaCategory;v_sg=0;v_fg=0;v_fpa=FUTURE"
tools = Tools(RunMode.RUN)


def accept_cookies():
    input('Accept Cookies')


def open_all_exhibitors():
    if tools.run_mode == RunMode.RUN:
        while True:
            tools.scroll()
            show_more_css = '#onlineGuide > div > div.EWP5KKC-e-I > div:nth-child(1) > div:nth-child(2) > div.EWP5KKC-u-b > div.EWP5KKC-u-c > div'
            try:
                tools.click_css_link(show_more_css)
            except (ElementNotInteractableException, ElementClickInterceptedException, TimeoutException):
                break
    else:
        tools.scroll()
    input("Done???")
    tools.driver.execute_script("window.scrollTo(0, 0);")


def parse_exhibitor(ex: Exhibitor):
    css_name = '#onlineGuidePopup > div > div > div:nth-child(1) > div.EWP5KKC-y-r > div:nth-child(1) > div.EWP5KKC-y-Eb.EWP5KKC-H-c.EWP5KKC-y-b > div.EWP5KKC-y-Jb > div.EWP5KKC-y-Fb > div > div > div.gwt-HTML.EWP5KKC-y-tc.EWP5KKC-y-eb'
    css_name = '[itemprop="legalName"]'
    css_street = '#onlineGuidePopup > div > div > div:nth-child(1) > div.EWP5KKC-y-r > div:nth-child(1) > div.EWP5KKC-y-Eb.EWP5KKC-H-c.EWP5KKC-y-b > div.EWP5KKC-y-Jb > div.EWP5KKC-y-Fb > div > div > div:nth-child(3) > div:nth-child(1) > div:nth-child(1)'
    css_postcode = '#onlineGuidePopup > div > div > div:nth-child(1) > div.EWP5KKC-y-r > div:nth-child(1) > div.EWP5KKC-y-Eb.EWP5KKC-H-c.EWP5KKC-y-b > div.EWP5KKC-y-Jb > div.EWP5KKC-y-Fb > div > div > div:nth-child(3) > span.gwt-InlineLabel.EWP5KKC-y-qb'
    css_postcode = '[itemprop="postalCode"]'
    css_city = '#onlineGuidePopup > div > div > div:nth-child(1) > div.EWP5KKC-y-r > div:nth-child(1) > div.EWP5KKC-y-Eb.EWP5KKC-H-c.EWP5KKC-y-b > div.EWP5KKC-y-Jb > div.EWP5KKC-y-Fb > div > div > div:nth-child(3) > span:nth-child(3)'
    css_city = '[itemprop="addressLocality"]'
    css_country = '#onlineGuidePopup > div > div > div:nth-child(1) > div.EWP5KKC-y-r > div:nth-child(1) > div.EWP5KKC-y-Eb.EWP5KKC-H-c.EWP5KKC-y-b > div.EWP5KKC-y-Jb > div.EWP5KKC-y-Fb > div > div > div:nth-child(3) > div.gwt-Label.EWP5KKC-y-qb.EWP5KKC-y-tc'
    css_country = '[itemprop="addressCountry"]'
    css_url = '[itemprop="url"]'
    css_info = '#onlineGuidePopup > div > div > div:nth-child(1) > div.EWP5KKC-y-r > div:nth-child(2) > div > div.EWP5KKC-y-Jb > div.EWP5KKC-y-Fb > div > div.gwt-HTML'
    css_tel = '[itemprop="telephone"]'
    css_mail = '#onlineGuidePopup > div > div > div:nth-child(1) > div.EWP5KKC-y-r > div:nth-child(1) > div.EWP5KKC-y-Eb.EWP5KKC-H-c.EWP5KKC-y-b > div.EWP5KKC-y-Jb > div.EWP5KKC-y-Fb > div > div > div:nth-child(5) > div:nth-child(4) > a'
    css_fax = '[itemprop="faxNumber"]'

    ex.name = tools.get_information_from_css_link(css_name)
    ex.url = tools.get_information_from_css_link(css_url)
    ex.tel = tools.get_information_from_css_link(css_tel)
    ex.mail = tools.get_information_from_css_link(css_mail)
    ex.fax = tools.get_information_from_css_link(css_fax)

    ex.street = tools.get_information_from_css_link(css_street)
    ex.postcode = tools.get_information_from_css_link(css_postcode)
    ex.city = tools.get_information_from_css_link(css_city)
    ex.country = tools.get_information_from_css_link(css_country)

    info = tools.get_information_from_css_link(css_info)

    ex.add_info(info)

    if tools.run_mode == RunMode.TESTING:
        print(str(ex))


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
