import time

from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor

exhibitor_list_link = "https://robau.inrostock.de/ausstellende-und-hallenplan/"
tools = Tools(RunMode.RUN)


def accept_cookies():
    css_accept = 'button.brlbs-cmpnt-btn brlbs-cmpnt-font-semibold brlbs-cmpnt-w-full brlbs-btn-accept-only-essential'.replace(' ', '.')
    tools.click_css_link(css_accept)


def get_exhibitor_links():

    links = []
    filter_str = 'https://robau.inrostock.de/aussteller/'
    prefix = ''
    i = 2
    while True:
        links += [prefix + l for l in tools.find_links(filter_str=filter_str)]

        css_link = f'button.page-button[data-page="{i}"]'
        try:
            tools.scroll()
            tools.click_css_link(css_link)
            time.sleep(4)
        except Exception:
            break
        i += 1


    return links


def parse_exhibitor(ex: Exhibitor):
    css_name = 'body > div.main-content > section.custom-page-intro > div > div.col-lg-8 > h1'
    css_data = 'div#exhibitor-details'

    timeout = 0.1
    ex.name = tools.get_information_from_css_link(css_name)

    data: list[str] = tools.get_information_from_css_link(css_data, timeout=timeout).splitlines()
    address_index = data.index('Anschrift')
    branch_index = data.index('Branche')
    contact_index = data.index('Kontakt')
    web_index = data.index('Web')

    ex.sort_address(data[address_index+1:branch_index])

    contact = data[contact_index+1:web_index]
    for c in contact:
        info = c.replace('Tel:', '').replace('E-Mail:', '').replace('Fax:', '')
        ex.sort_string(info)

    ex.url = data[web_index+1]
    pass



if __name__ == "__main__":
    tools.open_link(exhibitor_list_link)
    accept_cookies()
    time.sleep(1)
    tools.driver.maximize_window()
    time.sleep(1)
    links = tools.get_links(get_exhibitor_links)
    tools.iterate_exhibitor_links(links, parse_exhibitor)
