import time

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor

exhibitor_list_link = "https://exhibitors.iaa-transportation.com/showfloor#organization"
tools = Tools(RunMode.RUN)


def accept_cookies():
    css_accept = ''
    tools.click_css_link(css_accept)




def get_exhibitor_links():
    links = tools.get_saved_links()
    if len(links) != 0:
        return links

    css_letter = 'div.sc-cewOZc.bfuaCk'
    elements = tools.get_elements_by_css(css_letter)


    filter_str = '/company/'
    prefix = 'https://exhibitors.iaa-transportation.com'

    for el in elements[1:]: # iterate through all letters
        el.click()
        input('Scroll down, then press enter')
        links += [prefix + l for l in tools.find_links(filter_str=filter_str)]

    tools.save_links(links)
    return links


def parse_exhibitor(ex: Exhibitor):
    css_address = 'div.sc-kTfNwa.sc-jXnhOB'
    css_contact = 'div.container-fluid'
    css_info = 'p.sc-bDtxZQ.fmIdVB.mt-3'

    time.sleep(0.5)
    scroll_element(css_address)


    address = tools.get_information_from_css_link(css_address, timeout=20, throw_exception=True)
    address = address.splitlines()
    ex.name = address[0]
    ex.sort_list(address[1:])

    contact = tools.get_information_from_css_link(css_contact, timeout=0.5).splitlines()
    ex.sort_list(contact)

    info = tools.get_information_from_css_link(css_info, timeout=0.5)
    ex.add_info(info)

    if tools.run_mode == RunMode.TESTING:
        print(str(ex))

def scroll_element(css_link):
    scrollable_element = tools.driver.find_element(By.CSS_SELECTOR, css_link)
    element_size = scrollable_element.size
    scroll_x = element_size['width'] // 2
    scroll_y = element_size['height'] // 2
    action = ActionChains(tools.driver)
    action.move_to_element(scrollable_element).move_by_offset(scroll_x, scroll_y).release().perform()

if __name__ == "__main__":
    tools.open_link(exhibitor_list_link)
    links = get_exhibitor_links()
    print(f'Parse {len(links)} exhibitors')
    for link in links:
        exhibitor: Exhibitor = Exhibitor()
        try:
            tools.open_link(link)
            parse_exhibitor(exhibitor)
        except Exception:
            tools.log_error(link)
        finally:
            tools.save_exhibitor(exhibitor)
