from selenium.common.exceptions import TimeoutException

from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor

exhibitor_list_link = "https://www.ausstellungsverzeichnis.com/?page_id=662"
tools = Tools(RunMode.RUN)

def parse_exhibitor(ex: Exhibitor, index: int):
    index_str = f'{index}.even' if index % 2 == 0 else f'{index}.odd'
    css_name = f'#tablepress-19 > tbody > tr.row-{index_str} > td.column-1'
    css_info = f'#tablepress-19 > tbody > tr.row-{index_str} > td.column-3'
    css_mail = f'#tablepress-19 > tbody > tr.row-{index_str} > td.column-2 > a'

    ex.name = tools.get_information_from_css_link(css_name, throw_exception=True)
    ex.sort_string(tools.get_information_from_css_link(css_mail, timeout=0.5))

    info = tools.get_information_from_css_link(css_info, timeout=0.5)

    ex.add_info(info)

    if tools.run_mode == RunMode.TESTING:
        print(str(ex))


if __name__ == "__main__":
    tools.open_link(exhibitor_list_link)
    input("")
    for index in range(2,100):
        exhibitor: Exhibitor = Exhibitor()
        try:
            parse_exhibitor(exhibitor, index)
        except Exception:
            tools.log_error(str(index))
        finally:
            tools.save_exhibitor(exhibitor)

