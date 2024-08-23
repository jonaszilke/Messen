from selenium.common.exceptions import TimeoutException

from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor

exhibitor_list_link = "https://www.caravan-salon.de/kati-cgi/kati/vis/custom/ext2/download.cgi?ticket=$ticket&lang=%3Cdim_it::lang/%3E&fair=caravan2024&dl=html"
tools = Tools(RunMode.RUN)


def parse_exhibitor(ex: Exhibitor, i: int):
    css_name = f'body > table > tbody > tr:nth-child({i}) > td:nth-child(1)'
    css_postcode = f'body > table > tbody > tr:nth-child({i}) > td:nth-child(3)'
    css_city = f'body > table > tbody > tr:nth-child({i}) > td:nth-child(4)'


    ex.name = tools.get_information_from_css_link(css_name)
    ex.postcode = tools.get_information_from_css_link(css_postcode, timeout=0.5)
    ex.city = tools.get_information_from_css_link(css_city, timeout=0.5)


    if tools.run_mode == RunMode.TESTING:
        print(str(ex))


if __name__ == "__main__":
    tools.open_link(exhibitor_list_link)
    for index in range(2,879):
        exhibitor: Exhibitor = Exhibitor()
        try:
            parse_exhibitor(exhibitor, index)
        except TimeoutException:
            tools.log_error(str(index))
        finally:
            tools.save_exhibitor(exhibitor)
