import time

from selenium.common.exceptions import TimeoutException

from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor

prefix = 'https://www.thetire-cologne.de'
exhibitor_list_link = prefix + "/ttc-aussteller/ausstellerverzeichnis/"
number_of_pages = 23
tools = Tools(RunMode.RUN)


def accept_cookies():
    css_accept = '#onetrust-accept-btn-handler'
    tools.click_css_link(css_accept)


def get_exhibitor_links():
    links = tools.get_saved_links()
    if len(links) != 0:
        return links

    i = 2
    while True:
        print(i)
        css_toggle = '#ausform > div > div.notmobile > div > div.left > div > div > div > div.toggle'
        loaded = tools.wait_for_element(css_toggle, timeout=60)
        if not loaded and i < number_of_pages:
            print('komische seite')
            i -= 1
            tools.open_link(exhibitor_list_link)
        elif not loaded:
            print('break')
            break
        filter_str = '/aussteller/'
        links += [prefix + l for l in tools.find_links(filter_str=filter_str)]

        try:
            tools.click_css_link(css_toggle)
            css_page = f'#ausform > div > div.notmobile > div > div.left > div > div > div > div.select_options > div > div:nth-child({i}) > span > a'
            tools.click_css_link(css_page)
        except TimeoutException:
            print('nreak 2')
            break
        i += 1


    links = list(set(links))
    tools.save_links(links)
    return links


def parse_exhibitor(ex: Exhibitor):
    css_name = 'div.headline-title'
    css_address = '#top > div.main > div.maincontent > section > div:nth-child(3) > div > div > div > div.asdb54-detailseite-unternehmensinfo.asdb54-detailseite-greybox.inner.invertedback.clfix > div > div.imgAndInfo > div.info-holder > div.text-compound > div.text-left > div > div:nth-child(2)'
    css_url = 'a.xsecondarylink'
    css_info = 'div.werbetext54'

    ex.name = tools.get_information_from_css_link(css_name, throw_exception=True)
    ex.url = tools.get_information_from_css_link(css_url, timeout=0.5)

    address = tools.get_information_from_css_link(css_address, timeout=0.5)
    ex.sort_address(address.splitlines())

    info = tools.get_information_from_css_link(css_info, timeout=0.5)

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
            links.append(link)
            print(f'Couldnt open {link}')
            tools.reload_driver()
            time.sleep(120)
            tools.open_link(exhibitor_list_link)
            accept_cookies()
        finally:
            tools.save_exhibitor(exhibitor)


