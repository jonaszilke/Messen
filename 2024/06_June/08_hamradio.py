from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException

from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor

exhibitor_list_link = "https://www.hamradio-friedrichshafen.de/messe-programm/ausstellerverzeichnis"
tools = Tools(RunMode.RUN)


def accept_cookies():
    input("Accept Cookies manually")


def get_exhibitor_links():
    links = tools.get_saved_links()
    if len(links) != 0:
        return links

    tools.scroll()
    while True:
        filter_str = r'https://www.hamradio-friedrichshafen.de/messe-programm/ausstellerverzeichnis/aussteller'
        links += tools.find_links(filter_str=filter_str)
        css_next = '#exhibitor-app > div.paging.right > div.next'
        try:
            tools.click_css_link(css_next)
        except ElementClickInterceptedException:
            break


    tools.save_links(links)
    return links


def parse_exhibitor(ex: Exhibitor):
    css_name = '#wrapper > main > section.slim.ce-headline > div > div > div > div > div.text > h1'
    css_address = 'div.position'
    css_url = 'a.link.link-website'
    css_info = 'div.teaser'
    css_tel = 'a.link.link-phone'
    css_mail = 'a.link.link-email'
    css_fax = 'a.link.link-fax'

    ex.name = tools.get_information_from_css_link(css_name)
    ex.url = tools.get_href_from_css_link(css_url, timeout=0.5)
    ex.tel = tools.get_information_from_css_link(css_tel, timeout=0.5)
    mail = tools.get_href_from_css_link(css_mail, timeout=0.5)
    ex.mail = mail.replace('mailto:', '')
    ex.fax = tools.get_information_from_css_link(css_fax, timeout=0.5)

    address = tools.get_information_from_css_link(css_address).splitlines()
    ex.sort_address(address)

    info = tools.get_information_from_css_link(css_info)

    ex.add_info(info)
    ex.add_info(';'.join(address))

    if tools.run_mode == RunMode.TESTING:
        print(str(ex))


if __name__ == "__main__":
    tools.open_link(exhibitor_list_link)
    tools.driver.maximize_window()
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
