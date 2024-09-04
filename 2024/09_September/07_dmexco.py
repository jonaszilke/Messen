from selenium.common.exceptions import TimeoutException

from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor

exhibitor_list_link = "https://dmexco.com/de/ausstellerverzeichnis/"
exhibitor_list_link_2 = "https://community.dmexco.com/widget/event/dmexco-2024/exhibitors/RXZlbnRWaWV3XzgyMTMyMg==?showActions=true"
tools = Tools(RunMode.RUN)


def accept_cookies():
    css_accept = 'button.btn.btn--black.btn--default'
    tools.click_css_link(css_accept)


def get_exhibitor_links():
    links = tools.get_saved_links()
    if len(links) != 0:
        return links

    tools.scroll()
    filter_str = '/widget/event/dmexco-2024/exhibitor'
    prefix = 'https://community.dmexco.com'
    links = [prefix + l for l in tools.find_links(filter_str=filter_str)]

    tools.save_links(links)
    return links


def parse_exhibitor(ex: Exhibitor):
    css_name = 'h1.sc-c418aba9-7.dbnofQ'
    css_information = 'a.sc-5a4b0056-0.ircVKv'
    css_info = 'div.sc-dd6f9f7c-0.bFvNGm'

    ex.name = tools.get_information_from_css_link(css_name)

    elements = tools.get_elements_by_css(css_information)
    all_inf = [elem.text for elem in elements]

    if len(all_inf) == 0:
        return

    if all_inf[-1].find(',') != -1:
        address_full = all_inf.pop(-1)
        address = address_full.splitlines()[-1]
        address = address.split(',')
        address = list(dict.fromkeys(address)) # remove duplicates
        if len(address) == 2:
            ex.city = address[0]
            ex.country = address[1]
        else:
            ex.sort_address(address)

    for inf in all_inf:
        ex.sort_string(inf)
    # ex.url = tools.get_information_from_css_link(css_url, timeout=0.5)
    # ex.tel = tools.get_information_from_css_link(css_tel, timeout=0.5)
    # ex.mail = tools.get_information_from_css_link(css_mail, timeout=0.5)
    # ex.fax = tools.get_information_from_css_link(css_fax, timeout=0.5)
    #
    # ex.street = tools.get_information_from_css_link(css_street, timeout=0.5)
    # ex.postcode = tools.get_information_from_css_link(css_postcode, timeout=0.5)
    # ex.city = tools.get_information_from_css_link(css_city, timeout=0.5)
    # ex.country = tools.get_information_from_css_link(css_country, timeout=0.5)
    #
    info = tools.get_information_from_css_link(css_info, timeout=0.5)
    # ['https://advertising.amazon.com', 'München, Deutschland']
    ex.add_info(info)

    if tools.run_mode == RunMode.TESTING:
        print(str(ex))


if __name__ == "__main__":
    tools.open_link(exhibitor_list_link)
    accept_cookies()
    tools.open_link(exhibitor_list_link_2)
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
