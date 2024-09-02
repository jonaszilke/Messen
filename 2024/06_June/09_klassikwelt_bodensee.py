from selenium.common.exceptions import TimeoutException

from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor

exhibitor_list_link = "https://www.klassikwelt-bodensee.de/messeinformation/ausstellerverzeichnis/ausstellerverzeichnis"
tools = Tools(RunMode.RUN)


def accept_cookies():
    input("Accepted??")


def get_exhibitor_links():
    links = tools.get_saved_links()
    if len(links) != 0:
        return links

    links = get_links()

    tools.save_links(links)
    return links


def get_links():
    prefix = 'https://www.klassikwelt-bodensee.de'
    filter_str = '/messeinformation/ausstellerverzeichnis/ausstellerverzeichnis\?'
    links_letter = [prefix + l for l in tools.find_links(filter_str=filter_str)]

    links = []
    for link_letter in links_letter:
        tools.open_link(link_letter)
        filter_str = '/messeinformation/ausstellerverzeichnis/ausstellerverzeichnis/detail\?'
        links += [prefix + l for l in tools.find_links(filter_str=filter_str)]

    return links


def parse_exhibitor(ex: Exhibitor):
    css_name = '#c78378 > div > div.row.elementTeaser > div.col-xs-12.col-sm-9 > h1'
    css_street = ''
    css_postcode = ''
    css_city = ''
    css_country = ''
    css_url = ''
    css_info = '#c78378 > div > div.elementKontakt > div > div.col-xs-12.col-sm-6.col-md-6.contactleft'
    css_tel = ''
    css_mail = ''
    css_fax = ''

    ex.name = tools.get_information_from_css_link(css_name)
    ex.url = tools.get_information_from_css_link(css_url, timeout=0.5)
    ex.tel = tools.get_information_from_css_link(css_tel, timeout=0.5)
    ex.mail = tools.get_information_from_css_link(css_mail, timeout=0.5)
    ex.fax = tools.get_information_from_css_link(css_fax, timeout=0.5)

    ex.street = tools.get_information_from_css_link(css_street, timeout=0.5)
    ex.postcode = tools.get_information_from_css_link(css_postcode, timeout=0.5)
    ex.city = tools.get_information_from_css_link(css_city, timeout=0.5)
    ex.country = tools.get_information_from_css_link(css_country, timeout=0.5)

    info = tools.get_information_from_css_link(css_info, timeout=0.5)

    for inf in info.splitlines():
        ex.sort_string(inf.replace('Telefon:', '').replace('Telefax:', ''))

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
