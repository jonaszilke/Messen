from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor

exhibitor_list_link = "https://www.interboot.de/ausstellerverzeichnis/aussteller-marken"
tools = Tools(RunMode.RUN)


def accept_cookies():
    input('Accept')


def get_exhibitor_links():

    links = []
    tools.scroll()
    while True:
        try:
            filter_str = r'https://www.interboot.de/ausstellerverzeichnis/aussteller\?id='
            prefix = ''
            links += [prefix + l for l in tools.find_links(filter_str=filter_str)]
            css_next = 'div.next'
            tools.click_css_link(css_next)
        except Exception as e:
            break

    return links


def parse_exhibitor(ex: Exhibitor):
    css_name = '#wrapper > main > section.slim.ce-headline > div > div > div > div > div.text > h1'
    css_address = 'div.position'
    css_url = 'a.link.link-email'
    css_info = 'div.ce-bodytext'
    css_tel = 'a.link.link-phone'
    css_mail = 'a.link.link-email'
    css_fax = 'a.link.link-fax'

    ex.name = tools.get_information_from_css_link(css_name, throw_exception=True)
    ex.url = tools.get_href_from_css_link(css_url, timeout=0.1)
    ex.tel = tools.get_information_from_css_link(css_tel, timeout=0.1)
    ex.mail = tools.get_href_from_css_link(css_mail, timeout=0.1).replace('mailto:', '')
    ex.fax = tools.get_information_from_css_link(css_fax, timeout=0.1)

    address = tools.get_information_from_css_link(css_address, timeout=0.1).splitlines()
    ex.sort_address(address)

    info = tools.get_information_from_css_link(css_info, timeout=0.1)

    ex.add_info(info)

    if tools.run_mode == RunMode.TESTING:
        print(str(ex))


if __name__ == "__main__":
    tools.open_link(exhibitor_list_link)
    accept_cookies()
    links = tools.get_links(get_exhibitor_links)
    tools.iterate_exhibitor_links(links, parse_exhibitor)
