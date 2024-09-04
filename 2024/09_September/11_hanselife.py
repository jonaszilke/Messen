from selenium.common.exceptions import TimeoutException

from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor

exhibitor_list_link = "https://messebremen.ungerboeck.com/PROD/app85.cshtml?aat=49445436335838595073486a71736b784941646b30777a796a7a744a616d6d4269675846543178564641513d"
tools = Tools(RunMode.RUN)


def accept_cookies():
    css_accept = ''  
    tools.click_css_link(css_accept)


def get_exhibitor_links():
    links = tools.get_saved_links()
    if len(links) != 0:
        return links

    # tools.scroll()
    filter_str = ''
    prefix = ''
    links = [prefix + l for l in tools.find_links(filter_str=filter_str)]

    tools.save_links(links)
    return links


def parse_exhibitor(ex: Exhibitor):
    css_info_text = '#appBody > ux-dialog-container > div > div > div > div.modal-body > section.exhibitor-introduction > div:nth-child(2) > p'
    css_all_info = 'div.exhibitor-info'

    all_info = tools.get_information_from_css_link(css_all_info, timeout=30, throw_exception=True).splitlines()


    remove_list = ['Besuchen Sie unsere Website', 'Kontakt Informationen']
    for s in remove_list:
        if s in all_info:
            all_info.remove(s)

    ex.name = all_info[0]
    ex.sort_list(all_info)

    info = tools.get_information_from_css_link(css_info_text, timeout=0.5)

    ex.add_info(info)

    if ex.city[-5:].isdigit():
        ex.postcode = ex.city[-5:]
        ex.city = ex.city[:-6]

    if tools.run_mode == RunMode.TESTING:
        print(str(ex))


if __name__ == "__main__":
    tools.open_link(exhibitor_list_link)
    tools.scroll()
    i = 3
    while True:
        exhibitor: Exhibitor = Exhibitor()
        css_exhibitor = f'#vfpSection > section > table > tbody > tr:nth-child({i})'
        css_close = 'svg.svg-inline--fa.fa-xmark'
        try:
            tools.click_css_link(css_exhibitor)
            parse_exhibitor(exhibitor)
            tools.click_css_link(css_close)
        except TimeoutException:
            tools.log_error(f'{i}: {exhibitor.name}')
        finally:
            tools.save_exhibitor(exhibitor)
            i += 1
