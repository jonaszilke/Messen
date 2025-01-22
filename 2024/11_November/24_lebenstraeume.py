import time

from selenium.common import NoSuchElementException, TimeoutException

from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor

exhibitor_list_link = "https://www.lebenstraeume-grafschaft.de/aussteller/"
tools = Tools(RunMode.RUN)


def accept_cookies():
    time.sleep(2)


def get_exhibitor_links():

    links = []
    css_link = 'button.zm_default_inverse'
    elements = tools.get_elements_by_css(css_link)
    for element in elements:

        links.append(element.get_attribute('href'))

    return links


def parse_exhibitor(ex: Exhibitor):
    css_name = 'h4.single-post-headline'
    timeout = 0.1
    ex.name = tools.get_information_from_css_link(css_name)

    i = 1
    while True:
        css_text = f'div.col-md-8 > main > p:nth-child({i})'
        try:
            text = tools.get_information_from_css_link(css_text, timeout=timeout)
        except (NoSuchElementException, TimeoutException):
            break
        if text == 'Zur Website':
            css_url = f'div.col-md-8 > main > p:nth-child({i}) > a'
            ex.url = tools.get_href_from_css_link(css_url)
            break
        i += 1
        if i == 50:
            break





if __name__ == "__main__":
    tools.open_link(exhibitor_list_link)
    accept_cookies()
    links = tools.get_links(get_exhibitor_links)
    tools.iterate_exhibitor_links(links, parse_exhibitor)
