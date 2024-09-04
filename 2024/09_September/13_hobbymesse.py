import time

from selenium.common.exceptions import TimeoutException

from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor

exhibitor_list_link = "https://www.hobbymesse.de/de/aussteller-produkte/?limitSearchResults=10"
tools = Tools(RunMode.RUN)


def accept_cookies():
    css_accept = 'span#cmpbntyestxt'
    tools.click_css_link(css_accept)


def get_exhibitor_links():
    links = tools.get_saved_links()
    if len(links) != 0:
        return links

    css_load_all = 'body > div:nth-child(7) > div.main-content > div > section:nth-child(6) > div > section:nth-child(3) > div:nth-child(2) > div > button'
    tools.click_css_link(css_load_all)
    filter_str = '/aussteller-produkte/aussteller/hobbymesse/'
    prefix = 'https://www.hobbymesse.de'
    links = [prefix + l for l in tools.find_links(filter_str=filter_str)]

    tools.save_links(links)
    return links


def parse_exhibitor(ex: Exhibitor):

    css_data = 'div.company-contact.sticky-content.sticky-content--below-onpage-nav.flow'
    css_info = 'div.main-content__col.main-content__col--left > section:nth-child(2) > div > div:nth-child(1)'


    data = tools.get_information_from_css_link(css_data, throw_exception=True)
    data = data.replace('Tel.:', '').replace('Fax:', '')
    data = data.splitlines()

    remove_list = ['Kontakt', 'Aussteller kontaktieren', 'Ihre Ansprechpartner']
    for s in remove_list:
        if s in data:
            data.remove(s)

    ex.name = data[0]
    ex.sort_list(data[1:])

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
