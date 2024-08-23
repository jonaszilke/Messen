from selenium.common.exceptions import TimeoutException

from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor

exhibitor_list_link = "https://www.surface-technology-germany.de/de/ausstellung/ausstellerliste/?letter=a"
tools = Tools(RunMode.RUN)


def accept_cookies():
    css_accept = '#econda-pp2-banner-accept-all-channels-button'
    tools.click_css_link(css_accept)


def get_exhibitor_links():
    links = tools.get_saved_links()
    if len(links) != 0:
        return links

    import string
    for letter in list(string.ascii_lowercase):
        ex_link = f'https://www.surface-technology-germany.de/de/ausstellung/ausstellerliste/?letter={letter}'
        tools.open_link(ex_link)
        filter_str = '/aussteller/'
        prefix = 'https://www.surface-technology-germany.de'
        links += [prefix + l for l in tools.find_links(filter_str=filter_str)]

    tools.save_links(links)
    return links


def parse_exhibitor(ex: Exhibitor):
    css_name = 'h2.t.set-250-bold.as-headline'
    css_address = 'ul.t.set-250-regular.as-copy'
    css_url = 'a.render-item-component.is-secondary'
    css_tel = '#tabs-top > div.tabs-track > div > div > div > div > div:nth-child(2) > ul'

    ex.name = tools.get_information_from_css_link(css_name)
    ex.url = tools.get_href_from_css_link(css_url, timeout=0.5)
    phone_fax = tools.get_information_from_css_link(css_tel, timeout=0.5).splitlines()
    for inf in phone_fax:
        if 'Telefon:' in inf:
            ex.tel = inf.replace('Telefon:', '').strip()
        elif 'Fax:' in inf:
            ex.fax = inf.replace('Fax:', '').strip()

    address = tools.get_information_from_css_link(css_address, timeout=0.5).splitlines()
    ex.sort_address(address)

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
