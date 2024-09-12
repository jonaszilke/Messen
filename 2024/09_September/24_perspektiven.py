from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor

exhibitor_list_link = "https://www.messe-perspektiven.de/de/unternehmen/"
tools = Tools(RunMode.RUN)


def accept_cookies():
    css_accept = 'button.cc-btn.success'
    tools.click_css_link(css_accept)


def get_exhibitor_links():

    links = []
    filter_str = 'de/unternehmen/details/'
    prefix = 'https://www.messe-perspektiven.de/'
    css_next = 'li.next'
    while True:
        links += [prefix + l for l in tools.find_links(filter_str=filter_str)]
        try:
            tools.click_css_link(css_next)
        except Exception:
            break


    return links


def parse_exhibitor(ex: Exhibitor):
    css_name = '#article-6057 > div > div > div > div.head > div.left > h1'
    css_url = ''
    css_info = 'div.tab-content'
    css_tel = ''  
    css_mail = ''  
    css_fax = ''  
    css_data = 'div.person'

    timeout = 0.1
    ex.name = tools.get_information_from_css_link(css_name)
    ex.url = tools.get_information_from_css_link(css_url, timeout=timeout)
    ex.tel = tools.get_information_from_css_link(css_tel, timeout=timeout)
    ex.mail = tools.get_information_from_css_link(css_mail, timeout=timeout)
    ex.fax = tools.get_information_from_css_link(css_fax, timeout=timeout)

    data = tools.get_information_from_css_link(css_data, timeout=timeout).splitlines()
    ex.name = data[0]
    ex.sort_address(data[1:])

    info = tools.get_information_from_css_link(css_info, timeout=timeout)

    ex.add_info(info)


if __name__ == "__main__":
    tools.open_link(exhibitor_list_link)
    accept_cookies()
    links = tools.get_links(get_exhibitor_links)
    tools.iterate_exhibitor_links(links, parse_exhibitor)
