from selenium.common.exceptions import TimeoutException

from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor

exhibitor_list_link = "https://www.stanztec-messe.de/ausstellerverzeichnis/"
tools = Tools(RunMode.RUN)


def accept_cookies():
    css_accept = '._brlbs-btn._brlbs-btn-accept-all._brlbs-cursor'
    tools.click_css_link(css_accept)


def get_exhibitor_links():
    links = tools.get_saved_links()
    if len(links) != 0:
        return links

    # tools.scroll()
    filter_str = ''
    links = tools.find_links(filter_str=filter_str)

    tools.save_links(links)
    return links


def parse_exhibitor(ex: Exhibitor, index: int):
    css_address = f'#row-unique-0 > div > div > div.wpb_column.pos-top.pos-center.align_left.column_parent.col-lg-7.single-internal-gutter > div > div > div > div > div > div:nth-child({index}) > div > div.nftext > div > div:nth-child(1)'
    css_contact = f'#row-unique-0 > div > div > div.wpb_column.pos-top.pos-center.align_left.column_parent.col-lg-7.single-internal-gutter > div > div > div > div > div > div:nth-child({index}) > div > div.nftext > div > div:nth-child(2)'

    address = tools.get_information_from_css_link(css_address).splitlines()
    ex.name = address[0]
    ex.sort_address(address[1:])

    contact = tools.get_information_from_css_link(css_contact, timeout=0.5).splitlines()
    for inf in contact:
        ex.sort_string(inf.replace('Telefon:', '').replace('E-Mail:', ''))



    if tools.run_mode == RunMode.TESTING:
        print(str(ex))


if __name__ == "__main__":
    tools.open_link(exhibitor_list_link)
    accept_cookies()
    for page_num in range(1,3):
        ex_link = f'https://www.stanztec-messe.de/ausstellerverzeichnis/?pg={page_num}'
        tools.open_link(ex_link)
        for index in range(5, 105):
            exhibitor: Exhibitor = Exhibitor()
            try:
                parse_exhibitor(exhibitor, index)
            except TimeoutException:
                tools.log_error(f'{index}: {exhibitor.name}')
            finally:
                tools.save_exhibitor(exhibitor)
