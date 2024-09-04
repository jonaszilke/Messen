from selenium.common.exceptions import TimeoutException

from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor
import string

exhibitor_list_link = "https://www.galabau-messe.com/de-de/aussteller-produkte/aussteller-finden"
tools = Tools(RunMode.RUN)


def accept_cookies():
    css_accept = 'span#cmpwelcomebtnyes'
    tools.click_css_link(css_accept)


def get_exhibitor_links():
    links = tools.get_saved_links()
    if len(links) != 0:
        return links

    tools.scroll()
    for letter in string.ascii_lowercase:

        filter_str = f'/de-de/aussteller-produkte/{letter}/'
        prefix = 'https://www.galabau-messe.com'
        links += [prefix + l for l in tools.find_links(filter_str=filter_str)]

    tools.save_links(links)
    return links


def parse_exhibitor(ex: Exhibitor):
    css_name = 'h1.exhibitor-title'
    css_street = '#content > div > div:nth-child(2) > div > div > div.company-page.company-profile > div > div > div.info-container.inner-text.col-12.col-lg-4 > div:nth-child(2)'
    css_postcode = '#content > div > div:nth-child(2) > div > div > div.company-page.company-profile > div > div > div.info-container.inner-text.col-12.col-lg-4 > div:nth-child(3) > span:nth-child(1)'
    css_city = '#content > div > div:nth-child(2) > div > div > div.company-page.company-profile > div > div > div.info-container.inner-text.col-12.col-lg-4 > div:nth-child(3) > span:nth-child(2)'
    css_country = '#content > div > div:nth-child(2) > div > div > div.company-page.company-profile > div > div > div.info-container.inner-text.col-12.col-lg-4 > div:nth-child(4)'
    css_contact = 'div.contact-information'
    css_info = 'span.expandable-text'



    ex.name = tools.get_information_from_css_link(css_name)
    ex.street = tools.get_information_from_css_link(css_street, timeout=0.5)
    ex.postcode = tools.get_information_from_css_link(css_postcode, timeout=0.5)
    ex.city = tools.get_information_from_css_link(css_city, timeout=0.5)
    ex.country = tools.get_information_from_css_link(css_country, timeout=0.5)

    contact = tools.get_information_from_css_link(css_contact, timeout=0.5).splitlines()
    contact.remove('E-Mail senden')
    for c in contact:
        c_replace = c.replace('Tel.:', '').replace('Fax.:', '')
        ex.sort_string(c_replace)


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
        except Exception:
            tools.log_error(link)
        finally:
            tools.save_exhibitor(exhibitor)
