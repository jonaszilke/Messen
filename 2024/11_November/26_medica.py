import time
from datetime import datetime

from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor

exhibitor_list_link = "https://www.medica.de/vis/v1/de/directory/a"
tools = Tools(RunMode.RUN)


def accept_cookies():
    input('Accept Cookies manually!!!')



def get_exhibitor_links():

    links = []
    filter_str = '/vis/v1/de/exhprofiles/'
    prefix = 'https://www.medica.de'
    import string
    for letter in list(string.ascii_lowercase) + ['other']:
        link = f'https://www.medica.de/vis/v1/de/directory/{letter}'
        tools.open_link(link)
        links += [prefix + l for l in tools.find_links(filter_str=filter_str)]

    return links


def parse_exhibitor(ex: Exhibitor):
    css_name = 'h1.profile-head__name.profile-head__name--has-info'
    css_street = 'div.address-street'
    css_postcode = 'span.address-zip'
    css_city = 'span.address-city'
    css_country = 'div.address-country'
    css_url = 'div.link-list.link-list--slim'
    css_tel = 'div.exh-contact__phone'
    css_mail = 'div.exh-contact__email'

    timeout = 0.1
    ex.name = tools.get_information_from_css_link(css_name, throw_exception=True)

    css_show_contact_inf = '#finder-profile > div > div > section > div > div > div.profile-grid__content.profile-grid__content--secondary > section:nth-child(2) > div > button > div > span'
    try:
        tools.click_css_link(css_show_contact_inf)
        time.sleep(0.5)
    except Exception:
        pass
    ex.url = tools.get_information_from_css_link(css_url, timeout=timeout)
    ex.tel = tools.get_information_from_css_link(css_tel, timeout=timeout).replace('Telefon:', '')
    ex.mail = tools.get_information_from_css_link(css_mail, timeout=timeout).replace('E-Mail', '')

    ex.street = tools.get_information_from_css_link(css_street, timeout=timeout)
    ex.postcode = tools.get_information_from_css_link(css_postcode, timeout=timeout)
    ex.city = tools.get_information_from_css_link(css_city, timeout=timeout)
    ex.country = tools.get_information_from_css_link(css_country, timeout=timeout)

def get_failed_links():
    with open(tools.log_file_path, 'r') as file:
        link_list = [link.replace('\n', '') for link in file.readlines() if link != '\n']
        link_list = list(set(link_list))
    time_now = datetime.now().strftime('%Y%m%d_%H%M')
    new_save_path = tools.log_file_path[:-4] + f'_{time_now}.txt'
    tools.save_links(links=link_list, path=new_save_path)
    tools.remove_old_log_file()
    return link_list

if __name__ == "__main__":
    tools.open_link(exhibitor_list_link)
    accept_cookies()
    links = tools.get_links(get_exhibitor_links)
    tools.iterate_exhibitor_links(links, parse_exhibitor)
    failed_links = get_failed_links()
    while len(failed_links) > 0:
        print('-----------------------')
        print('NEW ITERATION')
        print('-----------------------')
        tools.iterate_exhibitor_links(failed_links, parse_exhibitor)
        try:
            failed_links = get_failed_links()
        except FileNotFoundError:
            break

