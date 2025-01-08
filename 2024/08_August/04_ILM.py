from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor

exhibitor_list_link = "https://www.ilm-offenbach.de/aussteller"
tools = Tools(RunMode.RUN)


def accept_cookies():
    css_accept = 'span.cf1y60'
    tools.click_css_link(css_accept)


def parse_exhibitor(ex: Exhibitor):
    css_address = 'div.anschrift'
    css_contact = 'div.Kontakt'

    address = tools.get_information_from_css_link(css_address, timeout=0.5).splitlines()[1:]
    contact = tools.get_information_from_css_link(css_contact, timeout=0.5).splitlines()[1:]

    ex.name = address[0]
    ex.sort_address(address[-3:])

    for data in contact:
        if data.startswith('Telefon:'):
            ex.tel = data.replace('Telefon:', '')
        if data.startswith('E-Mail:'):
            ex.mail = data.replace('E-Mail:', '')
        if data.startswith('Internet:'):
            ex.url = data.replace('Internet:', '')
        if data.startswith('Fax:'):
            ex.fax = data.replace('Fax:', '')

    for a in address:
        ex.add_info(a)
    for c in contact:
        ex.add_info(c)

    if tools.run_mode == RunMode.TESTING:
        print(str(ex))


def get_letter_buttons():
    parent_div = tools.driver.find_element(By.CSS_SELECTOR, 'div.flex.flex-wrap.mt-4.gap-x-4.gap-y-3', )
    buttons = parent_div.find_elements(By.TAG_NAME, 'button')
    filtered_buttons = [button for button in buttons if button.get_attribute('class') == '']
    return filtered_buttons

def get_details_buttons():
    return tools.driver.find_elements(By.CSS_SELECTOR, 'button.mt-4.underline')


if __name__ == "__main__":
    tools.open_link(exhibitor_list_link)
    accept_cookies()
    filtered_buttons = get_letter_buttons()
    for letter_button in filtered_buttons:
        tools.driver.execute_script("arguments[0].scrollIntoView(true);", letter_button)
        tools.driver.execute_script("window.scrollBy(0, -100);")
        letter_button.click()
        details_buttons = get_details_buttons()
        for detail_button in details_buttons:
            exhibitor: Exhibitor = Exhibitor()
            try:
                detail_button.click()
                parse_exhibitor(exhibitor)
                css_close = 'button.fixed.z-40.mr-0.text-5xl.w-7.h-7'
                tools.click_css_link(css_close)
            except TimeoutException:
                tools.log_error(exhibitor.name)
            finally:
                tools.save_exhibitor(exhibitor)
