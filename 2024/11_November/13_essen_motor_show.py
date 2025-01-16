import time

from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor

exhibitor_list_link = "https://www.essen-motorshow.de/automobilmesse/ausstellerliste/"
tools = Tools(RunMode.RUN)


def accept_cookies():
    css_accept = 'button.uc-btn.uc-btn-primary'
    tools.click_css_link(css_accept)


def get_exhibitor_links():
    tools.scroll()
    links = []
    filter_str = '/automobilmesse/ausstellerliste/detail/'
    prefix = 'https://www.essen-motorshow.de'
    links += [prefix + l.replace('\n', '').strip() for l in tools.find_links(filter_str=filter_str)]

    return links


def parse_exhibitor(ex: Exhibitor):
    time.sleep(1)
    css_name = 'div > div:nth-child(1) > h2'
    css_address = 'address'

    css_url = '#zeile_aussteller_infoblock > div > div.col.first > div > div.col.first > div > ul > li:nth-child(1) > a'


    timeout = 0.1
    ex.name = tools.get_information_from_css_link(css_name, throw_exception=True)

    url_text = tools.get_information_from_css_link(css_url, timeout=timeout)
    if url_text == 'Homepage':
        ex.url = tools.get_href_from_css_link(css_url)


    address = tools.get_information_from_css_link(css_address, timeout=timeout).splitlines()
    ex.sort_address(address)

    #get socials
    for i in range(1,4):
        css = f'#zeile_aussteller_infoblock > div > div.col.first > div > div.col.last > div > ul > li:nth-child({i})'
        social = tools.get_information_from_css_link(css, timeout=timeout)
        if social == 'E-Mail':
            css = f'#zeile_aussteller_infoblock > div > div.col.first > div > div.col.last > div > ul > li:nth-child({i}) > a'
            social = tools.get_href_from_css_link(css, timeout=timeout).replace('mailto:', '')
        ex.sort_string(social)

    if tools.run_mode == RunMode.TESTING:
        print(ex.name)


if __name__ == "__main__":
    tools.open_link(exhibitor_list_link)
    accept_cookies()
    links = tools.get_links(get_exhibitor_links)
    tools.iterate_exhibitor_links(links, parse_exhibitor)
