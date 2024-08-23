from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, \
    ElementNotInteractableException

from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor

exhibitor_list_link = "https://www.feuertrutz.de/aussteller-suche"
tools = Tools(RunMode.RUN)


def accept_cookies():
    input("Accept Cookies")


def get_exhibitor_links():
    links = tools.get_saved_links()
    if len(links) != 0:
        return links

    while True:
        tools.scroll()
        css_more = '#main > div.section.content.search-results.search-results-ausstellerverzeichnis > div > div > div > div.col-12.col-lg-8 > div:nth-child(2) > div > button'
        try:
            tools.click_css_link(css_more)
        except (TimeoutException, ElementNotInteractableException, ElementClickInterceptedException):
            break

    filter_str = ''
    links = tools.find_links(filter_str=filter_str)
    prefix = 'https://www.feuertrutz.de'
    links_2 = []
    for l in links:
        if l.startswith('/aussteller/'):
            links_2.append(prefix + l)
        elif l.isdigit():
            links_2.append(prefix + '/' + l)
    tools.save_links(links_2)
    return links_2

def is_exhibitor_link(link: str):
    return link.startswith('/aussteller/') or link.isdigit()


def parse_exhibitor(ex: Exhibitor):
    css_contact = 'div.row.address-info-box.mb-20'
    css_info = 'div.text-content'

    full_contact = tools.get_information_from_css_link(css_contact, throw_exception=True).replace('T: ', '').replace('F: ', '').splitlines()
    ex.name = full_contact[0]
    for inf in full_contact[1:]:
        ex.sort_string(inf)
        ex.add_info(inf)

    info = tools.get_information_from_css_link(css_info, timeout=0.5)
    ex.add_info(info)

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
