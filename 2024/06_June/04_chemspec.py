from selenium.common.exceptions import TimeoutException

from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor


tools = Tools(RunMode.RUN)


def accept_cookies():
    tools.click_css_link( '#onetrust-accept-btn-handler')


def get_exhibitor_links():
    if tools.run_mode == RunMode.RUN:
        tools.scroll()
    links = tools.find_links(filter_str='https://www.chemspeceurope.com/en-gb/exhibitor-details')
    links = [l for l in links if l.endswith('.html')] # remove double links
    return links


def parse_exhibitor():
    css_name = '#exhibitor-details > div > div.relative-position.white-space-no-wrap > div.details-header-wrapper > div > h1'
    css_adresse = '#exhibitor-details > div > div.row > div.col-md-4 > div.right-column-section.row > div:nth-child(2)'
    css_adresse_2 = '#exhibitor_details_address'
    css_url = '#exhibitor_details_website > p > a'
    css_info = '#exhibitor-details > div > div.row > div.col-md-8'
    css_tel = '#exhibitor_details_phone > p > a'
    css_mail = '#exhibitor_details_email > p > a'

    exhibitor = Exhibitor()
    exhibitor.name = tools.get_information_from_css_link(css_name, throw_exception=True)
    exhibitor.url = tools.get_href_from_css_link(css_url, timeout=1)
    exhibitor.tel = tools.get_information_from_css_link(css_tel, timeout=1)
    exhibitor.mail = tools.get_information_from_css_link(css_mail, timeout=1)

    try:
        address = tools.get_information_from_css_link(css_adresse, throw_exception=True, timeout=2)
    except TimeoutException:
        address = tools.get_information_from_css_link(css_adresse_2, throw_exception=True, timeout=2)
    address_full = address.replace('\n', ';')
    address_split = address.split('\n')
    exhibitor.street = address_split[1]
    exhibitor.country = address_split[-1]
    exhibitor.postcode = address_split[-2]
    exhibitor.city = address_split[-3]

    exhibitor.add_info(address_full)
    if tools.run_mode == RunMode.TESTING:
        print(str(exhibitor))
    return exhibitor



if __name__ == "__main__":
    tools.open_link("https://www.chemspeceurope.com/en-gb/exhibitor-list.html#/")
    tools.driver.maximize_window()
    accept_cookies()
    links = get_exhibitor_links()
    for link in links:
        try:
            tools.open_link(link)
            exhibitor: Exhibitor = parse_exhibitor()
            tools.save_exhibitor(exhibitor)
            if tools.run_mode == RunMode.TESTING:
                break
        except TimeoutException:
            tools.log_error(link)
