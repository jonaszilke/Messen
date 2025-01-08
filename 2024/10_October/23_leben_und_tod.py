from selenium.common.exceptions import TimeoutException

from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor

exhibitor_list_link = "https://www.leben-und-tod.de/besuchen-freiburg/"
tools = Tools(RunMode.RUN)


def accept_cookies():
    input('Accept Cookies and reject newsletter')


def expand_exhibitors():
    css_button = 'button#btnLoadMoreAussteller.button.button_size_2.button_dark'
    while True:
        try:
            tools.click_css_link(css_button, timeout=1)
        except TimeoutException:
            return



def parse_exhibitor(ex: Exhibitor, index: int):
    css_name = f'#ausstellerliste > div.section_wrapper.mfn-wrapper-for-wraps.mcb-section-inner.mcb-section-inner-1055f6000 > div > div > div.column.mcb-column.mcb-item-c18c7afd6.one.laptop-one.tablet-one.mobile-one.column_column > div > div > div > div.ausstellerliste.list-style > div:nth-child({index}) > div.item-aussteller-infos > h4'
    css_city = f'#ausstellerliste > div.section_wrapper.mfn-wrapper-for-wraps.mcb-section-inner.mcb-section-inner-1055f6000 > div > div > div.column.mcb-column.mcb-item-c18c7afd6.one.laptop-one.tablet-one.mobile-one.column_column > div > div > div > div.ausstellerliste.list-style > div:nth-child({index}) > div.item-aussteller-infos > span'
    css_url = f'#ausstellerliste > div.section_wrapper.mfn-wrapper-for-wraps.mcb-section-inner.mcb-section-inner-1055f6000 > div > div > div.column.mcb-column.mcb-item-c18c7afd6.one.laptop-one.tablet-one.mobile-one.column_column > div > div > div > div.ausstellerliste.list-style > div:nth-child({index}) > div.aussteller-kontakt-infos > div.kontakt-buttons > a:nth-child(1)'
    css_mail = f'#ausstellerliste > div.section_wrapper.mfn-wrapper-for-wraps.mcb-section-inner.mcb-section-inner-1055f6000 > div > div > div.column.mcb-column.mcb-item-c18c7afd6.one.laptop-one.tablet-one.mobile-one.column_column > div > div > div > div.ausstellerliste.list-style > div:nth-child({index}) > div.aussteller-kontakt-infos > div.kontakt-buttons > a:nth-child(2)'

    timeout = 0.1
    ex.name = tools.get_information_from_css_link(css_name)
    ex.url = tools.get_href_from_css_link(css_url, timeout=timeout)
    ex.mail = tools.get_href_from_css_link(css_mail, timeout=timeout).replace('mailto:', '')

    postcode_city = tools.get_information_from_css_link(css_city, timeout=timeout)
    country_city = postcode_city.split(' - ')

    ex.split_save_code_city(country_city[-1])
    ex.country = country_city[0] if len(country_city) > 1 else ''

if __name__ == "__main__":
    tools.open_link(exhibitor_list_link)
    accept_cookies()
    expand_exhibitors()
    error_counter = 0
    i = 1
    while True:
        exhibitor: Exhibitor = Exhibitor()
        try:
            parse_exhibitor(exhibitor, i)
            error_counter = 0
        except Exception:
            tools.log_error(exhibitor.name)
            error_counter += 1
            if error_counter > 5:
                break
        finally:
            tools.save_exhibitor(exhibitor, print_name=True)
            i += 1
