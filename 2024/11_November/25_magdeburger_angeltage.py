from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor

exhibitor_list_link = "https://www.magdeburger-angeltage.de/de/ausstellerverzeichnis/"
tools = Tools(RunMode.RUN)


def accept_cookies():
    css_accept = 'button.cc-btn.success'
    try:
        tools.click_css_link(css_accept)
    except:
        input('Accept Cookies manually!!!')


def get_exhibitor_links():

    links = []
    filter_str = 'de/ausstellerverzeichnis/ausstellerdetail/'
    prefix = 'https://www.magdeburger-angeltage.de/'
    links += [prefix + l for l in tools.find_links(filter_str=filter_str)]

    return links


def parse_exhibitor(ex: Exhibitor):
    css_name = 'h2.name'
    css_address = 'div.address'
    css_url = 'p.homepage'

    timeout = 0.1
    ex.name = tools.get_information_from_css_link(css_name)
    ex.url = tools.get_information_from_css_link(css_url, timeout=timeout)

    address = tools.get_information_from_css_link(css_address, timeout=timeout).splitlines()
    ex.sort_address(address)



if __name__ == "__main__":
    tools.open_link(exhibitor_list_link)
    accept_cookies()
    links = tools.get_links(get_exhibitor_links)
    tools.iterate_exhibitor_links(links, parse_exhibitor)
