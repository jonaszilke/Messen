import time

from selenium.common import TimeoutException

from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor

exhibitor_list_link = "https://www.offerta.de/offerta-live/ausstellendenverzeichnis/"
tools = Tools(RunMode.RUN)


def accept_cookies():
    try:
        css_accept = 'button.sc-dcJsrY.dDGQLz'
        tools.click_css_link(css_accept)
    except TimeoutException:
        input('Accept Cokies')



def parse_exhibitor(ex: Exhibitor, idx: int):
    css_name = f'#__nuxt > div > div > div > div > div > main > div > div > section > div > div > div > div > div:nth-child(2) > section.exhibitor-register__search-results > div:nth-child({idx}) > section > header > h3'
    css_street = f'#__nuxt > div > div > div > div > div > main > div > div > section > div > div > div > div > div:nth-child(2) > section.exhibitor-register__search-results > div:nth-child({idx}) > section > main > div.exhibitor-register__search-result__contact > div.mb-4'
    css_url = f'#__nuxt > div > div > div > div > div > main > div > div > section > div > div > div > div > div:nth-child(2) > section.exhibitor-register__search-results > div:nth-child({idx}) > section > main > div.exhibitor-register__search-result__contact > div:nth-child(3) > a > span'


    ex.name = tools.get_information_from_css_link(css_name)
    ex.url = tools.get_information_from_css_link(css_url)

    address = tools.get_information_from_css_link(css_street).split(',')
    ex.sort_address(address)

if __name__ == "__main__":
    tools.open_link(exhibitor_list_link)
    accept_cookies()
    for idx in range(1,594):
        css_show_ex = f'#__nuxt > div > div > div > div > div > main > div > div > section > div > div > div > div > div:nth-child(2) > section.exhibitor-register__search-results > div:nth-child({idx}) > section > header > button'
        tools.click_css_link(css_show_ex)
        time.sleep(1)
        exhibitor: Exhibitor = Exhibitor()
        try:
            parse_exhibitor(exhibitor, idx)
        except Exception:
            tools.log_error(str(idx))
        finally:
            tools.save_exhibitor(exhibitor)
