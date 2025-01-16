import time

from selenium.common.exceptions import TimeoutException

from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor

exhibitor_list_link = "https://messebremen.ungerboeck.com/PROD/app85.cshtml?aat=667935796167634b4c55706d674d2f6644757539676175474b736f5075674938627155537979324d5369513d"
tools = Tools(RunMode.RUN)



def parse_exhibitor(ex: Exhibitor):
    css_info_text = '#appBody > ux-dialog-container > div > div > div > div.modal-body > section.exhibitor-introduction > div:nth-child(2) > p'
    css_all_info = 'div.exhibitor-info'

    all_info = tools.get_information_from_css_link(css_all_info, timeout=30, throw_exception=True).splitlines()


    remove_list = ['Besuchen Sie unsere Website', 'Kontakt Informationen', 'Auf dem Hallenplan anzeigen']
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

    css_list = '#sidebar > ul > li:nth-child(1) > div.title.au-target > span'
    tools.click_css_link(css_list)
    time.sleep(3)
    i = 3
    while True:
        exhibitor: Exhibitor = Exhibitor()
        css_exhibitor = f'#exhibitorList > li:nth-child({i}) > div > div.booth-title.au-target' #exhibitorList > li:nth-child(3)
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
