from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor

exhibitor_list_link = "https://www.domizil-husum.de/fuer-besucher/ausstellerliste"
tools = Tools(RunMode.RUN)


def accept_cookies():
    css_accept = '#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll'
    tools.click_css_link(css_accept)


def get_exhibitor_links():

    links = []
    filter_str = '/fuer-besucher/ausstellerliste/detail/'
    prefix = 'https://www.domizil-husum.de'

    for i in range(1,27):
        css_letter = f'#exhibitorFilter > div.col-12.col-lg > ul > li:nth-child({i})'
        tools.click_css_link(css_letter)
        links += [prefix + l for l in tools.find_links(filter_str=filter_str)]

    return links


def parse_exhibitor(ex: Exhibitor):
    css_name = 'h1.mb-3'
    css_address = 'div.address'
    css_contact = '#c324 > div > div > div > div > div.col-12.col-md-8 > div > div:nth-child(2) > p'


    timeout = 0.1
    ex.name = tools.get_information_from_css_link(css_name)
    address = tools.get_information_from_css_link(css_address, timeout=timeout).splitlines()

    contact = tools.get_information_from_css_link(css_contact, timeout=timeout).splitlines()

    ex.sort_address(address)
    ex.sort_list(contact)
    if tools.run_mode == RunMode.TESTING:
        print(str(ex))

if __name__ == "__main__":
    tools.open_link(exhibitor_list_link)
    accept_cookies()
    links = tools.get_links(get_exhibitor_links)
    tools.iterate_exhibitor_links(links, parse_exhibitor)
