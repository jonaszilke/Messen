from selenium.common.exceptions import TimeoutException

from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor

exhibitor_list_link = "https://www.gamescom.global/de/partners"
tools = Tools(RunMode.TESTING)


def accept_cookies():
    css_accept = '#onetrust-accept-btn-handler'
    tools.click_css_link(css_accept, timeout=20)


def get_exhibitor_links():
    links = tools.get_saved_links()
    if len(links) != 0:
        return links

    tools.scroll()
    filter_str = '/de/partner/'
    prefix = 'https://www.gamescom.global'
    links = [prefix + l for l in tools.find_links(filter_str=filter_str)]

    tools.save_links(links)
    return links


def parse_exhibitor(ex: Exhibitor):
    tools.scroll()
    css_name = 'div.owner-header__name.text-left'
    css_data = 'section.imprint'

    ex.name = tools.get_information_from_css_link(css_name)
    data = tools.get_information_from_css_link(css_data, throw_exception=False)
    data = data.splitlines()

    words = ['impressum', 'adresse', 'company']
    for d in data[1:]:
        if d.lower() not in words:
            info = d.replace('TEL:', '')
            ex.sort_string(info)


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
