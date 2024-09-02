import time

from selenium.common.exceptions import TimeoutException

from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor

exhibitor_list_link = "https://www.learntec.de/de/learntec/ausstellerliste/"
tools = Tools(RunMode.RUN)


def accept_cookies():
    input("Accept Cookies")

def get_exhibitor_links():
    links = tools.get_saved_links()
    if len(links) != 0:
        return links

    tools.scroll()
    filter_str = '/de/learntec/ausstellerliste/\?talque=sponsor'
    prefix = 'https://www.learntec.de'
    links = [prefix + l for l in tools.find_links(filter_str=filter_str)]

    tools.save_links(links)
    return links


def parse_exhibitor(ex: Exhibitor):
    css_name = 'h1.tq-inline.tq-align-middle'
    css_info = 'tq-markdown.the-description-text'


    ex.name = tools.get_information_from_css_link(css_name, throw_exception=True)
    info = tools.get_information_from_css_link(css_info, timeout=0.5)


    i = 1
    stop = False
    while not stop:
        css_link = f'body > main > div:nth-child(2) > div.bottom.col-xs-12 > div:nth-child(2) > div:nth-child(1) > tq-plugin-view > tq-css-normalization > tq-vendor-id-plugin > tq-max-width-container > div > tq-vendor-details > div > div.tq-flex.tq-flex-row.sm\:tq-flex-col.tq-flex-grow.the-vendor-items.tq-order-2.sm\:tq-order-1 > div > div.the-vendor-details.tq-pt-2 > div > div.tq-flex.tq-flex-col > tq-stats-item:nth-child({i}) > a'
        css_link_2 = f'body > main > div:nth-child(2) > div.bottom.col-xs-12 > div:nth-child(2) > div:nth-child(1) > tq-plugin-view > tq-css-normalization > tq-vendor-id-plugin > tq-max-width-container > div > tq-vendor-details > div > div.tq-flex.tq-flex-row.sm\:tq-flex-col.tq-flex-grow.the-vendor-items.tq-order-2.sm\:tq-order-1 > div > div.the-vendor-details.tq-pt-2 > div > div.tq-flex.tq-flex-col > tq-stats-item:nth-child({i}) > div > a'
        try:
            ex.sort_string(tools.get_information_from_css_link(css_link, throw_exception=True, timeout=0.5))
        except TimeoutException:
            stop = True

        try:
            ex.sort_string(tools.get_information_from_css_link(css_link_2, throw_exception=True, timeout=0.5))
            stop = False
        except TimeoutException:
            pass

        i += 1

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
            time.sleep(2)
            parse_exhibitor(exhibitor)
        except TimeoutException:
            tools.log_error(link)
        finally:
            tools.save_exhibitor(exhibitor)
