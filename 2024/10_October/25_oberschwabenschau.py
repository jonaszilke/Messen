from selenium.common.exceptions import TimeoutException

from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor

exhibitor_list_link = "https://www.ausstellungsverzeichnis.com/?page_id=88"
tools = Tools(RunMode.RUN)


def parse_exhibitor(ex: Exhibitor, index: int):
    css_name = f'#tablepress-15 > tbody > tr.row-{index} > td.column-1'
    css_mail = f'#tablepress-15 > tbody > tr.row-{index} > td.column-2 > a'

    ex.name = tools.get_information_from_css_link(css_name, throw_exception=True)
    ex.sort_string(tools.get_information_from_css_link(css_mail, timeout=0.5))

    if tools.run_mode == RunMode.TESTING:
        print(str(ex))


if __name__ == "__main__":
    tools.open_link(exhibitor_list_link)
    counter = 0
    for _ in range(10):
        for index in range(2 + 50 * counter, 52 + 50 * counter):
            exhibitor: Exhibitor = Exhibitor()
            try:
                parse_exhibitor(exhibitor, index)
            except Exception:
                tools.log_error(str(index))
            finally:
                tools.save_exhibitor(exhibitor)
        css_next_page = 'button.dt-paging-button.next'
        tools.click_css_link(css_next_page)
        counter += 1
