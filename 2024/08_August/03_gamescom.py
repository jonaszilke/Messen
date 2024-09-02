from selenium.common.exceptions import TimeoutException

from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor

exhibitor_list_link = "https://www.gamescom.global/de/partners"
tools = Tools(RunMode.RUN)


def accept_cookies():
    css_accept = '#onetrust-accept-btn-handler'
    tools.click_css_link(css_accept, timeout=20)


def get_exhibitor_links():
    links = tools.get_saved_links()
    if len(links) != 0:
        return links

    tools.scroll()
    filter_str = '/de/aussteller/'
    prefix = 'https://exhibitors.gamescom.global'
    links = tools.find_links(filter_str=filter_str)
    # links = [prefix + l for l in links]

    tools.save_links(links)
    return links


def parse_exhibitor(ex: Exhibitor):
    css_name = 'div.headline-title'
    css_data = 'div.location-info'
    css_url = 'a.xsecondarylink '

    ex.name = tools.get_information_from_css_link(css_name, throw_exception=True)
    data = tools.get_information_from_css_link(css_data, throw_exception=False)
    data = data.splitlines()
    ex.url = tools.get_information_from_css_link(css_url, throw_exception=False, timeout=0.1)

    ex.sort_address(data)


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
            tools.reload_driver()
            tools.log_error(link)
            links.append(link)
            tools.open_link(exhibitor_list_link)
            accept_cookies()
        finally:
            tools.save_exhibitor(exhibitor)
