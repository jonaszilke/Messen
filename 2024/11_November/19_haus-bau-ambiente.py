import os.path
import time

from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor

exhibitor_list_link = "https://www.haus-bau-ambiente.de/aussteller/ausstellerliste/"
tools = Tools(RunMode.TESTING)


def accept_cookies():
    if tools.load_local_storage():
        tools.driver.refresh()
        return
    input('Accept')
    tools.save_local_storage()



def parse_exhibitor(ex: Exhibitor):
    css_address = 'div.pf-exhibitor__profile-adress'
    css_url = 'div.pf-exhibitor__hero-content > div.pf-exhibitor__hero-buttons > a:nth-child(3)'
    css_socials = 'div.pf-exhibitor__profile-links'

    timeout = 10
    ex.url = tools.get_href_from_css_link(css_url, timeout=timeout)

    address = tools.get_information_from_css_link(css_address, timeout=timeout).splitlines()
    ex.name = address[0]
    ex.sort_address(address[1:])

    socials = tools.get_information_from_css_link(css_socials, timeout=timeout).splitlines()
    ex.sort_list(socials)

def setup():
    tools.open_link(exhibitor_list_link)
    accept_cookies()
    # tools.scroll()
    tools.driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(3)

if __name__ == "__main__":

    setup()
    number_path = r'.\data\19_haus_bau_ambiente_numbers.txt'
    if not os.path.exists(number_path):
        with open(number_path, 'w') as f:
            f.write('')
    with open(number_path, 'r') as f:
        finished = [int(x) for x in f.read().splitlines()]

    i = 1
    counter = 0
    while True:
        if i in finished:
            i += 1
            continue
        css_exhibitor = f'div.pf-widget.pf-exhibitor > div > div.pf-exhibitor-grid > div.pf-exhibitor-content > div > div > div.pf-exhibitor-events__list > div:nth-child(1) > a > div > div > div.pf-flex-1'
        xpath_exhibitor = f'//*[@id="profairs-widget-exhibitor"]/div//div[1]/div/div[2]/div[2]/div/div/div[2]/div[1]/a/div/div/div[2]/div[2]'
        xpath_exhibitor = f'//*[@id="profairs-widget-exhibitor"]/div//div[1]/div/div[2]/div[2]/div/div/div[2]/div[{i}]/a/div/div/div[2]/div[2]'
        exhibitor: Exhibitor = Exhibitor()
        try:
            # tools.scroll_css_into_view(css_exhibitor, sleep_time=3)
            # tools.click_css_link(css_exhibitor)
            tools.click_xpath(xpath_exhibitor)
            time.sleep(1)
            parse_exhibitor(exhibitor)
            css_back = 'button.pf-exhibitor__back'
            tools.scroll_css_into_view(css_back)
            tools.click_css_link(css_back)
            time.sleep(1)
            counter = 0
            with open(number_path, 'a') as f:
                f.write(f'{i}\n')
        except Exception as e:
            tools.log_error(exhibitor.name)
            tools.reload_driver()
            setup()
            counter += 1
        finally:
            tools.save_exhibitor(exhibitor)
        if counter > 5:
            break
        i += 1
