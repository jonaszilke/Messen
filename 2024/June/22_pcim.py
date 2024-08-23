from selenium.common.exceptions import TimeoutException

from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor

exhibitor_list_link = "https://pcim.mesago.com/nuernberg/de/ausstellersuche.html"
tools = Tools(RunMode.RUN)


def accept_cookies():
    input("Accept Cookies")


def get_exhibitor_links():
    links = tools.get_saved_links()
    if len(links) != 0:
        return links

    tools.scroll()
    input("Scroll?")

    filter_str = '/nuernberg/de/ausstellersuche.detail.html'
    prefix = 'https://pcim.mesago.com'
    links = [prefix + l for l in tools.find_links(filter_str=filter_str)]

    tools.save_links(links)
    return links


def parse_exhibitor(ex: Exhibitor):
    css_full_contact = 'p.ex-contact-box__address-field-full-address'
    css_url = 'a.icon.icon-news-before.ex-contact-box__website-link'
    css_info = 'div.ex-text-image__copy'
    css_tel = 'a.a-link.ex-contact-box__address-field-tel-number'
    css_mail = 'a.ex-contact-box__contact-btn.btn.btn-primary'
    css_fax = 'span.ex-contact-box__address-field-fax-number'

    contact = tools.get_information_from_css_link(css_full_contact).splitlines()
    ex.name = contact[0]
    ex.sort_address(contact[1:])


    ex.url = tools.get_href_from_css_link(css_url, timeout=0.5)
    ex.tel = tools.get_information_from_css_link(css_tel, timeout=0.5)
    ex.mail = tools.get_href_from_css_link(css_mail, timeout=0.5).replace('mailto:', '').replace('?subject=PCIM%20Europe%202024', '')
    ex.fax = tools.get_information_from_css_link(css_fax, timeout=0.5).replace('Fax', '')



    info = tools.get_information_from_css_link(css_info, timeout=0.5)

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
