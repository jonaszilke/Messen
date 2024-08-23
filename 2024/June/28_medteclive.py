from selenium.common.exceptions import TimeoutException

from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor

exhibitor_list_link = "https://www.medteclive.com/de/aussteller-und-anbieter"
tools = Tools(RunMode.RUN)


def accept_cookies():
    css_accept = '#cmpbntyestxt'
    tools.click_css_link(css_accept)


def get_exhibitor_links():
    links = tools.get_saved_links()
    if len(links) != 0:
        return links

    tools.scroll()
    filter_str = '/de/p/'
    prefix = 'https://www.medteclive.com'
    links = [prefix + l for l in tools.find_links(filter_str=filter_str)]

    tools.save_links(links)
    return links


def parse_exhibitor(ex: Exhibitor):
    css_name = 'div.column.name'
    css_url = 'body > main > section:nth-child(3) > div > div > div.column.two-thirds-sidebar > ul > li:nth-child(2) > a'
    css_info = 'body > main > section:nth-child(3) > div > div > div.column.two-thirds-sidebar > p'


    ex.name = tools.get_information_from_css_link(css_name).replace('\nFolgen Merken', '')
    ex.url = tools.get_information_from_css_link(css_url, timeout=0.5)

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
