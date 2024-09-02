import time

from selenium.common.exceptions import TimeoutException

from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor

exhibitor_list_link = "https://outdoorexhibitors.ispo.com/onlinecatalog/2024/list-of-exhibitors/"
tools = Tools(RunMode.RUN)


def accept_cookies():
    input("Accept Cookies!!")




def get_exhibitor_links():
    links = tools.get_saved_links()
    if len(links) != 0:
        return links

    css_next = 'div.paging_RightArrows_cell'
    filter_str = 'https://outdoorexhibitors.ispo.com/onlinecatalog/2024/list-of-exhibitors/exhibitordetails'

    for _ in range(41):
        try:
            links += tools.find_links(filter_str=filter_str)
            tools.click_css_link(css_next)
            time.sleep(20)
        except TimeoutException:
            break

    tools.save_links(links)
    return links


def parse_exhibitor(ex: Exhibitor):
    css_name = 'div.ce_head'
    css_address = 'div.ce_addr'
    css_url = 'div.ce_website a'
    css_info = 'div.pb_ce'
    css_tel = 'div.ce_phone a'
    css_mail = 'div.ce_email a'

    ex.name = tools.get_information_from_css_link(css_name)
    ex.url = tools.get_information_from_css_link(css_url, timeout=0.5)
    ex.tel = tools.get_information_from_css_link(css_tel, timeout=0.5)
    ex.mail = tools.get_information_from_css_link(css_mail, timeout=0.5)

    address = tools.get_information_from_css_link(css_address, timeout=0.5)
    address_split = address.split(',')
    if len(address_split) == 3:
        ex.sort_address(address_split)
    elif len(address_split) < 3:
        ex.country = address_split[-1]
        ex.city = address_split[-2]
        ex.street = address_split[:-2]
    else:
        ex.street = address

    info = tools.get_information_from_css_link(css_info, timeout=0.5)

    ex.add_info(address)
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
