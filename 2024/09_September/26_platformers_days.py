from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor

exhibitor_list_link = "https://ausstellerverzeichnis.platformers-days.de/vis/v1/de/directory/a"
tools = Tools(RunMode.RUN)


def accept_cookies():
    input('Accept Cookies!!')



def get_exhibitor_links():

    links = []
    filter_str = '/vis/v1/de/exhibitors/'
    prefix = 'https://ausstellerverzeichnis.platformers-days.de'
    import string
    for letter in list(string.ascii_lowercase):
        link = f'https://ausstellerverzeichnis.platformers-days.de/vis/v1/de/directory/{letter}?oid=250&lang=1'
        tools.open_link(link)
        links += [prefix + l for l in tools.find_links(filter_str=filter_str)]

    return links


def parse_exhibitor(ex: Exhibitor):
    css_name = 'h1[itemprop="name"]'
    css_street = 'span[itemprop="streetAddress"]'
    css_postcode = 'span[itemprop="postalCode"]'
    css_city = 'span[itemprop="addressLocality"]'
    css_country = 'span[itemprop="addressCountry"]'
    css_url = 'a[itemprop="url"]'
    css_info = 'span[itemprop="streetAddress"]'
    css_tel = 'span[itemprop="telephone"]'
    css_mail = 'a[itemprop="email"]'
    css_fax = 'span[itemprop="faxNumber"]'

    timeout = 0.1
    ex.name = tools.get_information_from_css_link(css_name, throw_exception=True)
    ex.url = tools.get_information_from_css_link(css_url, timeout=timeout)
    ex.tel = tools.get_information_from_css_link(css_tel, timeout=timeout)
    ex.mail = tools.get_information_from_css_link(css_mail, timeout=timeout)
    ex.fax = tools.get_information_from_css_link(css_fax, timeout=timeout)

    ex.street = tools.get_information_from_css_link(css_street, timeout=timeout)
    ex.postcode = tools.get_information_from_css_link(css_postcode, timeout=timeout)
    ex.city = tools.get_information_from_css_link(css_city, timeout=timeout)
    ex.country = tools.get_information_from_css_link(css_country, timeout=timeout)

    info = tools.get_information_from_css_link(css_info, timeout=timeout)

    ex.add_info(info)

if __name__ == "__main__":
    tools.open_link(exhibitor_list_link)
    accept_cookies()
    links = tools.get_links(get_exhibitor_links)
    tools.iterate_exhibitor_links(links, parse_exhibitor)
