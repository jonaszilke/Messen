from selenium.common.exceptions import TimeoutException, ElementNotInteractableException, NoSuchElementException, \
    StaleElementReferenceException, ElementClickInterceptedException

from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor
from tqdm import tqdm
import time

exhibitor_list_link = "https://www.ifa-berlin.com/de/exhibitors"
tools = Tools(RunMode.RUN)


def accept_cookies():
    css_accept = 'button#onetrust-accept-btn-handler'
    tools.click_css_link(css_accept)


def get_exhibitor_links():
    links = []
    css_next = 'a.pagination__list__item__link.pagination__list__item__link--next'
    filter_str = 'exhibitors/'
    prefix = 'https://www.ifa-berlin.com/de/'
    while True:
        links += [prefix + l for l in tools.find_links(filter_str=filter_str)]
        try:
            tools.click_css_link(css_next, timeout=20)
        except (TimeoutException, ElementNotInteractableException, NoSuchElementException):
            break
        except StaleElementReferenceException as e:
            print(e.msg)
            time.sleep(1)
        except ElementClickInterceptedException as e:
            print(e.msg)
            time.sleep(1)

    return links


def parse_exhibitor(ex: Exhibitor):
    css_name = 'h2.m-exhibitor-entry__item__header__title'
    css_address = 'div.m-exhibitor-entry__item__header__meta__address'
    css_url = 'span.m-exhibitor-entry__item__header__social__item__link__text'
    css_info = 'div.m-exhibitor-entry__item__body__brand-info__body'


    ex.name = tools.get_information_from_css_link(css_name, throw_exception=True)
    url = tools.get_information_from_css_link(css_url, timeout=0.5)

    address = tools.get_information_from_css_link(css_address, timeout=0.5).splitlines()
    if len(address) == 3:
        ex.city = address[0]
        ex.postcode = address[1]
        ex.country = address[2]
    else:
        ex.sort_list(address)

    socials = ['youtube', 'tiktok', 'instagram', 'facebook']
    is_url = True
    for s in socials:
        if s in url.lower():
            is_url = False
    if is_url:
        ex.url = url

    info = tools.get_information_from_css_link(css_info, timeout=0.5)

    ex.add_info(info)

    if tools.run_mode == RunMode.TESTING:
        print(str(ex))


if __name__ == "__main__":
    tools.open_link(exhibitor_list_link)
    accept_cookies()
    links = tools.get_links(get_exhibitor_links)
    print(f'Parse {len(links)} exhibitors')
    it_list = tqdm(links) if tools.run_mode == RunMode.RUN else links
    with tqdm(total=len(links), position=0, leave=True, bar_format='{desc:<30}{percentage:3.0f}%|{bar:40}{r_bar}', colour='white') as pbar:
        for link in links:
            exhibitor: Exhibitor = Exhibitor()
            try:
                tools.open_link(link)
                parse_exhibitor(exhibitor)
            except TimeoutException:
                tools.log_error(link)
            finally:
                tools.save_exhibitor(exhibitor)
                new_desc = exhibitor.name + (50 * ' ')
                pbar.set_description(new_desc[:50])
                pbar.update(1)
