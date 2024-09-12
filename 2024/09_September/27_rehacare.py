from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor

exhibitor_list_link = "https://www.rehacare.de/vis/v1/de/directory/a?oid=43612&lang=1"
tools = Tools(RunMode.RUN)

rerun = True
def accept_cookies():
    input('Accept Cookies!!')



def get_exhibitor_links():

    links = []
    filter_str = '/vis/v1/de/exhprofiles/'
    prefix = 'https://www.rehacare.de'
    import string
    for letter in list(string.ascii_lowercase):
        link = f'https://www.rehacare.de/vis/v1/de/directory/{letter}?oid=43612&lang=1'
        tools.open_link(link)
        links += [prefix + l for l in tools.find_links(filter_str=filter_str)]

    return links

def get_error_links():
    error_path = r'C:\Users\jonas\PycharmProjects\Messen\2024\09_September\data\27_rehacare_error_log_2.txt'
    with open(error_path, 'r') as file:
        links = [link.replace('\n', '') for link in file.readlines() if link != '\n']
        links = list(set(links))
        return links
def parse_exhibitor(ex: Exhibitor):
    css_show_data = '#finder-profile > div > div > section > div > div > div.profile-grid__content.profile-grid__content--secondary > div.profile__cta-buttons > button > div'
    tools.click_css_link(css_show_data)

    css_name = '#profile-title > h1'
    css_street = 'div.address-street'
    css_postcode = 'span.address-zip'
    css_city = 'span.address-city'
    css_country = 'div.address-country'
    css_url = 'div.link-list.link-list--slim'
    css_info = 'div.profile-details-text'
    css_tel = 'div.exh-contact__phone'
    css_mail = 'div.exh-contact__email'


    timeout = 0.1
    ex.name = tools.get_information_from_css_link(css_name, throw_exception=True)
    ex.url = tools.get_information_from_css_link(css_url, timeout=timeout).replace('Web:', '')
    ex.tel = tools.get_information_from_css_link(css_tel, timeout=timeout).replace('Telefon:', '')
    ex.mail = tools.get_information_from_css_link(css_mail, timeout=timeout).replace('E-Mail:','')

    ex.street = tools.get_information_from_css_link(css_street, timeout=timeout)
    ex.postcode = tools.get_information_from_css_link(css_postcode, timeout=timeout)
    ex.city = tools.get_information_from_css_link(css_city, timeout=timeout)
    ex.country = tools.get_information_from_css_link(css_country, timeout=timeout)

    info = tools.get_information_from_css_link(css_info, timeout=timeout)

    ex.add_info(info)

if __name__ == "__main__":
    tools.open_link(exhibitor_list_link)
    accept_cookies()
    links = tools.get_links(get_exhibitor_links) if not rerun else get_error_links()
    tools.iterate_exhibitor_links(links, parse_exhibitor)