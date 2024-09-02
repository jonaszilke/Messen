from selenium.common.exceptions import TimeoutException

from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor

exhibitor_list_link = "https://exhibitors.ifat.de/de/aussteller-warengruppen/aussteller-marken?_gl=1*nxgqc6*_gcl_au*NTQ2NjIxOTQ3LjE3MjQ2Nzc1ODc.*_ga*NDU5MDQ0MjA1LjE3MjQ2Nzc1ODc.*_ga_YWCJ1X9ZBX*MTcyNDY3NzU4Ny4xLjAuMTcyNDY3NzU4Ny42MC4wLjA."
tools = Tools(RunMode.TESTING)


def accept_cookies():
    input('Accept Cookies!!')


def get_exhibitor_links():
    links = tools.get_saved_links()
    if len(links) != 0:
        return links

    while True:
        css_load_more = '#div_AusstellerTreffer > table > tbody > tr.lazymore > td'
        try:
            tools.scroll()
            tools.click_css_link(css_load_more, timeout=30)
        except TimeoutException:
            break
    filter_str = 'https://exhibitors.ifat.de/de/aussteller-warengruppen/aussteller-marken/aussteller-marken-details/exhibitorDetail/'
    prefix = ''
    links = [prefix + l for l in tools.find_links(filter_str=filter_str)]

    tools.save_links(links)
    return links


def parse_exhibitor(ex: Exhibitor):
    css_name = 'div.contentblock_firma'
    css_address = 'div.exhibitordetails-locationinfo'

    css_contact = 'div.exhibitordetails-contactinfo'

    ex.name = tools.get_information_from_css_link(css_name).replace('\n', '')

    address = tools.get_information_from_css_link(css_address, timeout=0.5).splitlines()[1:]
    ex.sort_address(address)

    contact = tools.get_information_from_css_link(css_contact)
    contact = contact.replace('E-Mail:', '').replace('Tel:', '').replace('Webseite:', '').replace('Fax:', '').splitlines()[1:]
    for c in contact:
        ex.sort_string(c)


    if tools.run_mode == RunMode.TESTING:
        print(str(ex))


if __name__ == "__main__":
    tools.open_link(exhibitor_list_link)
    accept_cookies()
    links = get_exhibitor_links()
    for link in links:
        exhibitor: Exhibitor = Exhibitor()
        try:
            tools.open_link(link)
            parse_exhibitor(exhibitor)
        except TimeoutException:
            tools.log_error(link)
        finally:
            tools.save_exhibitor(exhibitor)
