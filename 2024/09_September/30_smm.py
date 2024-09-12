from selenium.common import TimeoutException

from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor

exhibitor_list_link = "https://www.smm-hamburg.de/messe/ausstellende-produkte/ausstellendenverzeichnis"
tools = Tools(RunMode.RUN)


def accept_cookies():
    input('accept Cookies')


def get_exhibitor_links():
    links = []
    while True:
        css_load_more = 'div.d-md-flex.justify-content-center.mt-a'
        try:
            tools.click_css_link(css_load_more, timeout=10)
        except Exception:
            break
    filter_str = '/platform/SM24/corporation/'
    prefix = 'https://www.smm-hamburg.de'
    links += [prefix + l for l in tools.find_links(filter_str=filter_str)]

    return links


def parse_exhibitor(ex: Exhibitor):
    css_name = 'body > main > aside > article > div.mt-b.rmr-c.rmb-a.rml-c > section > div > div > header > div:nth-child(2) > h2'

    timeout = 0.1
    ex.name = tools.get_information_from_css_link(css_name, throw_exception=True)

    i = 2
    while True:
        css_link = f'body > main > aside > article > div.mt-b.rmr-c.rmb-a.rml-c > section > aside > ul > li:nth-child({i})'
        try:
            data = tools.get_information_from_css_link(css_link, throw_exception=True, timeout=timeout).splitlines()
        except TimeoutException:
            break
        if 'Adresse' in data:
            ex.sort_address(data[1:])
        elif 'Telefon' in data:
            ex.tel = data[1]
        elif 'Web' in data:
            css_url = f'body > main > aside > article > div.mt-b.rmr-c.rmb-a.rml-c > section > aside > ul > li:nth-child({i}) > ul > li:nth-child(1) > a'
            css_mail = f'body > main > aside > article > div.mt-b.rmr-c.rmb-a.rml-c > section > aside > ul > li:nth-child({i}) > ul > li:nth-child(2) > a'
            ex.url = tools.get_href_from_css_link(css_url, timeout=timeout)
            ex.mail = tools.get_href_from_css_link(css_mail, timeout=timeout).replace('mailto:','')
        else:
            break
        i += 1

if __name__ == "__main__":
    tools.open_link(exhibitor_list_link)
    accept_cookies()
    links = tools.get_links(get_exhibitor_links)
    tools.iterate_exhibitor_links(links, parse_exhibitor)
