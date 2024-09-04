from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor

exhibitor_list_link = ""  
tools = Tools(RunMode.TESTING)


def accept_cookies():
    css_accept = ''  
    tools.click_css_link(css_accept)


def get_exhibitor_links():

    links = []
    filter_str = ''
    prefix = ''
    links += [prefix + l for l in tools.find_links(filter_str=filter_str)]

    return links


def parse_exhibitor(ex: Exhibitor):
    css_name = ''  
    css_street = ''  
    css_postcode = ''  
    css_city = ''  
    css_country = ''  
    css_url = ''  
    css_info = ''  
    css_tel = ''  
    css_mail = ''  
    css_fax = ''  

    ex.name = tools.get_information_from_css_link(css_name)
    ex.url = tools.get_information_from_css_link(css_url, timeout=0.5)
    ex.tel = tools.get_information_from_css_link(css_tel, timeout=0.5)
    ex.mail = tools.get_information_from_css_link(css_mail, timeout=0.5)
    ex.fax = tools.get_information_from_css_link(css_fax, timeout=0.5)

    ex.street = tools.get_information_from_css_link(css_street, timeout=0.5)
    ex.postcode = tools.get_information_from_css_link(css_postcode, timeout=0.5)
    ex.city = tools.get_information_from_css_link(css_city, timeout=0.5)
    ex.country = tools.get_information_from_css_link(css_country, timeout=0.5)

    info = tools.get_information_from_css_link(css_info, timeout=0.5)

    ex.add_info(info)

    if tools.run_mode == RunMode.TESTING:
        print(str(ex))


if __name__ == "__main__":
    tools.open_link(exhibitor_list_link)
    accept_cookies()
    links = tools.get_links(get_exhibitor_links)
    tools.iterate_exhibitor_links(links, parse_exhibitor)
