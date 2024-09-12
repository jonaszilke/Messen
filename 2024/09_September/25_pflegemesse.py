import time

from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor

exhibitor_list_link = "https://www.inrostock.de/aussteller/?fair_taxonomy=29"
tools = Tools(RunMode.RUN)


def accept_cookies():
    css_accept = 'a._brlbs-btn._brlbs-btn-accept-all._brlbs-cursor'
    tools.click_css_link(css_accept)


def get_exhibitor_links():
    links = []
    filter_str = ''
    prefix = ''
    links += [prefix + l for l in tools.find_links(filter_str=filter_str)]

    return links


def parse_exhibitor(ex: Exhibitor, index: int):
    css_name = f'#site-content > div > div.contentbox > div > section > article:nth-child({index}) > div.titel'
    css_data = f'#site-content > div > div.contentbox > div > section > article:nth-child({index}) > div.kontakt'

    timeout = 0.1
    ex.name = tools.get_information_from_css_link(css_name, timeout=0.1, throw_exception=True)
    data = tools.get_information_from_css_link(css_data, timeout=timeout).splitlines()

    data_2 = []
    for d in data:
        data_2 += d.split('|')
    remove_list = ['Telefon:','Telefax:','E-Mail:','Website:']
    data_3 = []
    for i,d in enumerate(data_2):
        for r in remove_list:
            if r in d:
                data_2[i] = d.replace(r,'')

    ex.sort_list(data_2)
    pass

if __name__ == "__main__":
    tools.open_link(exhibitor_list_link)
    accept_cookies()
    time.sleep(3)
    counter = 0
    index = 3
    while True:
        exhibitor = Exhibitor()
        try:
            parse_exhibitor(exhibitor, index)
            counter = 0
        except Exception:
            counter += 1
        finally:
            index += 1
            tools.save_exhibitor(exhibitor)
        if counter > 3:
            break


#
# #site-content > div > div.contentbox > div > section > article:nth-child(4) > div.titel
# #site-content > div > div.contentbox > div > section > article:nth-child(6) > div.titel
# #site-content > div > div.contentbox > div > section > article:nth-child(8) > div.titel
# #site-content > div > div.contentbox > div > section > article:nth-child(3) > div.kontakt
