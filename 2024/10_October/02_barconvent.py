import time

from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor

exhibitor_list_link = "https://www.barconvent.com/de-de/fuer-besucher/Austellerliste.html#/"
tools = Tools(RunMode.RUN)


def accept_cookies():
    css_accept = 'button#onetrust-accept-btn-handler'
    tools.click_css_link(css_accept)
    css_adult = 'button.btn.btn-primary.btn-lg.btn-block'
    tools.click_css_link(css_adult)
    time.sleep(5)


def get_exhibitor_links():
    tools.scroll()

    links = []
    filter_str = 'https://www.barconvent.com/de-de/fuer-besucher/Austellerliste/exhibitordetails.'
    prefix = ''
    links += [prefix + l for l in tools.find_links(filter_str=filter_str)]

    return links


def parse_exhibitor(ex: Exhibitor):
    css_name = 'h1.wrap-word'


    css_address = '#exhibitor_details_address'
    css_tel = 'a[data-dtm="exhibitorDetails_phoneLink"]'
    css_mail = 'a[data-dtm="exhibitorDetails_emailLink"]'
    css_url = 'a[data-dtm="exhibitorDetails_externalLink"]'
    css_info = 'div#exhibitor_details_description'

    timeout = 0.1
    ex.name = tools.get_information_from_css_link(css_name)
    address = tools.get_information_from_css_link(css_address, timeout=timeout)
    ex.add_info(address) # save address in info text
    address = address.splitlines()[1:] # remove 'ANSCHRIFT'

    ex.country = address[-1]
    ex.street = address[0]

    ex.postcode = address[-2]
    ex.city = address[1]



    ex.tel = tools.get_information_from_css_link(css_tel, timeout=timeout)
    ex.mail = tools.get_information_from_css_link(css_mail, timeout=timeout)
    ex.url = tools.get_information_from_css_link(css_url, timeout=timeout)

    info = tools.get_information_from_css_link(css_info, timeout=timeout)

    ex.add_info(info)

if __name__ == "__main__":
    tools.open_link(exhibitor_list_link)
    accept_cookies()
    links = tools.get_links(get_exhibitor_links)
    tools.iterate_exhibitor_links(links, parse_exhibitor)
