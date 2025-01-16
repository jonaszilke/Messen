from selenium.common.exceptions import TimeoutException

from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor

exhibitor_list_link = "https://texcare.messefrankfurt.com/frankfurt/de/ausstellersuche.html"
tools = Tools(RunMode.RUN)


def accept_cookies():
    input("Accept Cookies and wait for banner and close it")


def get_exhibitor_links():
    css_num_pages = '#mf-ex-root > div > div > div:nth-child(2) > div > div.ex-exhibitor-search__content.h-background.h-background--fullwidth > div.ex-exhibitor-search__content_right > div.ex-exhibitor-search__container.o-search-results-container__results.ex-exhibitor-search__container_narrow > div > div.MF-REACT > div > button:nth-child(6) > span'
    num_pages = int(tools.get_information_from_css_link(css_num_pages))
    links = []

    for i in range(num_pages-1):
        elem = 7 if i < 3 or i> num_pages - 5 else 9

        filter_str = '/frankfurt/de/ausstellersuche.detail.html'
        prefix = 'https://texcare.messefrankfurt.com'
        links += [prefix + l for l in tools.find_links(filter_str=filter_str)]
        css_next = f'#mf-ex-root > div > div > div:nth-child(2) > div > div.ex-exhibitor-search__content.h-background.h-background--fullwidth > div.ex-exhibitor-search__content_right > div.ex-exhibitor-search__container.o-search-results-container__results.ex-exhibitor-search__container_narrow > div > div.MF-REACT > div > button:nth-child({elem})'
        try:
            tools.click_css_link(css_next)
        except TimeoutException:
            break
        time.sleep(2)

    return links


def parse_exhibitor(ex: Exhibitor):
    css_name = 'h1.ex-exhibitor-detail__title-headline'
    css_full_contact = 'p.ex-contact-box__address-field-full-address'
    css_url = 'a.icon.icon-news-before.ex-contact-box__website-link'
    css_info = 'div.ex-text-image__copy'
    css_tel = 'a.a-link.ex-contact-box__address-field-tel-number'
    css_mail = 'a.ex-contact-box__contact-btn.btn.btn-primary'
    css_fax = 'span.ex-contact-box__address-field-fax-number'

    ex.name = tools.get_information_from_css_link(css_name, timeout=20, throw_exception=True)
    contact = tools.get_information_from_css_link(css_full_contact, timeout=30, throw_exception=True).splitlines()
    ex.sort_address(contact[1:])


    ex.url = tools.get_href_from_css_link(css_url, timeout=0.5)
    ex.tel = tools.get_information_from_css_link(css_tel, timeout=0.5)
    mail = tools.get_href_from_css_link(css_mail, timeout=0.5).replace('mailto:', '')
    ex.email = mail[:mail.find('?')]
    ex.fax = tools.get_information_from_css_link(css_fax, timeout=0.5).replace('Fax', '')



    info = tools.get_information_from_css_link(css_info, timeout=0.5)

    ex.add_info(info)

    if tools.run_mode == RunMode.TESTING:
        print(str(ex))


if __name__ == "__main__":
    import time

    start_time = time.time()

    tools.open_link(exhibitor_list_link)
    accept_cookies()
    links = tools.get_links(get_exhibitor_links)
    tools.iterate_exhibitor_links(links, parse_exhibitor)
