import time

from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor

exhibitor_list_link = "https://www.veggieworld.eco/hamburg/"
tools = Tools(RunMode.RUN)


def accept_cookies():
    input('Accept Cookies!!!!')


def parse_exhibitor(ex: Exhibitor):
    css_name = 'address'
    css_url = 'span.web'
    css_tel = 'span.phone'
    css_mail = 'span.mail'

    timeout = 0.1
    address = tools.get_information_from_css_link(css_name).splitlines()
    ex.url = tools.get_information_from_css_link(css_url, timeout=timeout)
    ex.tel = tools.get_information_from_css_link(css_tel, timeout=timeout)
    ex.mail = tools.get_information_from_css_link(css_mail, timeout=timeout)

    ex.name = address[0]
    ex.sort_list(address[1:])


if __name__ == "__main__":

    tools.open_link(exhibitor_list_link)
    accept_cookies()

    css_logo = 'div.exhibitor-logo'
    logo_elements = tools.get_elements_by_css(css_logo)

    for e in logo_elements:
        exhibitor: Exhibitor = Exhibitor()
        try:
            tools.scroll_element_into_view(e)
            e.click()
            parse_exhibitor(exhibitor)
            css_close = 'span.close'
            tools.click_css_link(css_close)
            time.sleep(0.5)
        except:
            tools.log_error(exhibitor.name)
        finally:
            tools.save_exhibitor(exhibitor)
