from selenium.common import NoSuchElementException, TimeoutException

from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor

exhibitor_list_link = "https://www.get-nord.de/die-get-nord/ausstellende-produkte"
tools = Tools(RunMode.RUN)


def accept_cookies():
    css_accept = '#uc-center-container > div.sc-eBMEME.dRvQzh > div > div.sc-jsJBEP.iXSECa > div > button:nth-child(2)'
    try:
        tools.click_css_link(css_accept)
    except:
        input('Accept Cookies manually!!!')


def get_exhibitor_links():
    links = []
    css_show_more = '#c200040 > div > form > div.container-responsive.overflow-unset > div.hmc-platform-search__results > ul > div > div > a'
    while True:
        try:
            tools.scroll_css_into_view(css_show_more)
            tools.click_css_link(css_show_more)
        except (NoSuchElementException, TimeoutException):
            break

    filter_str = '/platform/GT24/corporation/'
    prefix = 'https://www.get-nord.de'
    links += [prefix + l for l in tools.find_links(filter_str=filter_str)]

    return links


def parse_exhibitor(ex: Exhibitor):
    css_name = 'body > main > aside > article > div.mt-b.rmr-c.rmb-a.rml-c > section > div > div > header > div:nth-child(2) > h2'
    css_address = 'body > main > aside > article > div.mt-b.rmr-c.rmb-a.rml-c > section > aside > ul > li:nth-child(2) > p'
    css_tel = 'body > main > aside > article > div.mt-b.rmr-c.rmb-a.rml-c > section > aside > ul > li:nth-child(3)'
    css_url = 'body > main > aside > article > div.mt-b.rmr-c.rmb-a.rml-c > section > aside > ul > li:nth-child(4) > ul > li:nth-child(1) > a'
    css_mail = 'body > main > aside > article > div.mt-b.rmr-c.rmb-a.rml-c > section > aside > ul > li:nth-child(4) > ul > li:nth-child(2) > a'
    css_fax = ''  

    timeout = 0.1
    ex.name = tools.get_information_from_css_link(css_name, throw_exception=True)

    for i in range(2,5):
        css_link = f'body > main > aside > article > div.mt-b.rmr-c.rmb-a.rml-c > section > aside > ul > li:nth-child({i})'
        inf = tools.get_information_from_css_link(css_link)
        if 'Adresse' in inf:
            address = inf.replace('Adresse', '').strip().splitlines()
            ex.sort_address(address)
        elif 'Telefon' in inf:
            ex.tel = inf.replace('Telefon', '').strip()
        elif 'Web' in inf:
            css_url = f'body > main > aside > article > div.mt-b.rmr-c.rmb-a.rml-c > section > aside > ul > li:nth-child({i}) > ul > li:nth-child(1) > a'
            css_mail = f'body > main > aside > article > div.mt-b.rmr-c.rmb-a.rml-c > section > aside > ul > li:nth-child({i}) > ul > li:nth-child(2) > a'
            inf_1 = tools.get_href_from_css_link(css_url, timeout=timeout)
            inf_2 = tools.get_href_from_css_link(css_mail, timeout=timeout)
            ex.sort_list([inf_1, inf_2])



if __name__ == "__main__":
    tools.open_link(exhibitor_list_link)
    accept_cookies()
    links = tools.get_links(get_exhibitor_links)
    tools.iterate_exhibitor_links(links, parse_exhibitor)
