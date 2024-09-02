from selenium.common.exceptions import TimeoutException

from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor

exhibitor_list_link = "https://www.sensor-test.de/de/besucher/suche-ap/exhibitors"
tools = Tools(RunMode.RUN)


def accept_cookies():
    css_accept = 'button.button.ccm--save-settings.ccm--button-primary.ccm--ctrl-init'
    tools.click_css_link(css_accept)


def get_exhibitor_links():
    links = tools.get_saved_links()
    if len(links) != 0:
        return links

    import string
    for letter in list(string.ascii_uppercase):
        ex_link = f'https://www.sensor-test.de/de/besucher/suche-ap/exhibitors/{letter}'
        tools.open_link(ex_link)

        filter_str = '/de/besucher/suche-ap/exhibitor/'
        prefix = 'https://www.sensor-test.de'
        links += [prefix + l for l in tools.find_links(filter_str=filter_str) if '#product-news' not in l]

    tools.save_links(links)
    return links


def parse_exhibitor(ex: Exhibitor):
    css_name = '.title-logo h2'
    css_address = 'div.address'
    css_postcode = ''  
    css_city = ''  
    css_country = ''  
    css_url = ''  
    css_info = '.exhibitor-catalogue-entry div.text-image p'
    css_tel = ''  
    css_mail = ''  
    css_fax = ''  

    ex.name = tools.get_information_from_css_link(css_name)

    data = tools.get_information_from_css_link(css_address, timeout=0.5).splitlines()

    for d in data:
        ex.sort_string(d)
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
