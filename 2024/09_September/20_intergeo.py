import time

from selenium.common import NoSuchElementException, TimeoutException, ElementNotInteractableException

from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor

exhibitor_list_link = "https://intergeo.by-qb.com/list/"
tools = Tools(RunMode.RUN)


def accept_cookies():
    css_accept = 'button.ccc-banner__button.ccc-banner__button--primary'
    tools.click_css_link(css_accept)


def parse_exhibitor(ex: Exhibitor):
    css_name = 'h2.fgc[data-key="title"]'
    css_street = 'p[data-key="street"]'
    css_postcode = 'span[data-key="zipcode"]'
    css_city = 'span[data-key="city"]'
    css_country = 'p[data-key="countryname"]'
    css_url = 'span[data-key="web"]'
    css_info = 'span[data-key="description"]'
    css_tel = 'span[data-key="phone"]'
    css_mail = ''  
    css_fax = 'span[data-key="fax"]'

    timeout = 0.1
    ex.name = tools.get_information_from_css_link(css_name)
    ex.url = tools.get_information_from_css_link(css_url, timeout=timeout)
    ex.tel = tools.get_information_from_css_link(css_tel, timeout=timeout)
    ex.mail = tools.get_information_from_css_link(css_mail, timeout=timeout)
    ex.fax = tools.get_information_from_css_link(css_fax, timeout=timeout)

    ex.street = tools.get_information_from_css_link(css_street, timeout=timeout)
    ex.postcode = tools.get_information_from_css_link(css_postcode, timeout=timeout)
    ex.city = tools.get_information_from_css_link(css_city, timeout=timeout)
    ex.country = tools.get_information_from_css_link(css_country, timeout=timeout)

    info = tools.get_information_from_css_link(css_info, timeout=timeout)

    ex.add_info(info)

    if tools.run_mode == RunMode.TESTING:
        print(str(ex))

def page():
    for i in range(1,21):
        css_exhibitor = f'#exhibitorListStart > section.main > ul > li:nth-child({i}) > h3'
        exhibitor = Exhibitor()
        try:
            tools.click_css_link(css_exhibitor)
            time.sleep(1)
            parse_exhibitor(exhibitor)
            time.sleep(1)
            tools.back()
            time.sleep(1)
        except Exception:
            tools.log_error(exhibitor.name)
        finally:
            tools.save_exhibitor(exhibitor)

if __name__ == "__main__":
    tools.open_link(exhibitor_list_link)
    input('done??')
    # accept_cookies()
    while True:
        page()
        css_next = 'i.btn-next.fa.fa-arrow-circle-o-right.fa-2x'
        try:
            tools.click_css_link(css_next)
        except (Exception, NoSuchElementException, ElementNotInteractableException, TimeoutException):
            break
