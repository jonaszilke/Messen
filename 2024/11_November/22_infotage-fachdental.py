import time

from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor

exhibitor_list_link = "https://www.messe-stuttgart.de/infotagefachdental-stuttgart/ausstellung/unternehmen-produkte/ausstellerverzeichnis#/"
tools = Tools(RunMode.RUN)


def accept_cookies():
    input('Accept Cookies!!')


def parse_exhibitor(ex: Exhibitor):
    css_info = '#detail-modal > div > div > div:nth-child(3) > div > div.ed-detail__segment.ed-detail__segment--contacts'

    data = tools.get_information_from_css_link(css_info, throw_exception=True).splitlines()
    ex.name = data[1]

    for d in data[2:]:
        ex.sort_string(d)

    if tools.run_mode == RunMode.TESTING:
        print(str(ex))


def get_redo_pairs():
    path = r'.\data\22_infotage-fachdental_error_log_redo.txt'
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()

    to_int = lambda x : (int(x[0]), int(x[1]))
    l = [l.strip().removeprefix('(').removesuffix('):').split(',') for l in lines]
    return list(map(to_int, l))

def redo():
    for i, j in get_redo_pairs():
        exhibitor: Exhibitor = Exhibitor()
        try:
            css_link = f'#ed-list > div.ed-characterGroupWrapper > div:nth-child({j}) > div:nth-child({i}) > div > div > a'
            tools.scroll_css_into_view(css_link)
            tools.click_css_link(css_link)
            parse_exhibitor(exhibitor)
            tools.back()
        except ElementClickInterceptedException:
            tools.log_error(f'({j},{i}): {exhibitor.name}')
        except (IndexError, TimeoutException):
            tools.log_error(f'({j},{i}): {exhibitor.name}')
            tools.back()
        except NoSuchElementException:
            pass
        finally:
            tools.save_exhibitor(exhibitor)


if __name__ == "__main__":
    tools.open_link(exhibitor_list_link)
    tools.driver.maximize_window()
    accept_cookies()
    tools.scroll()
    tools.driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(3)

    i = 2
    j = 1
    no_ex = 0
    while True:

        exhibitor: Exhibitor = Exhibitor()
        try:
            css_link = f'#ed-list > div.ed-characterGroupWrapper > div:nth-child({j}) > div:nth-child({i}) > div > div > a'
            tools.scroll_css_into_view(css_link)
            tools.click_css_link(css_link)
            parse_exhibitor(exhibitor)
            tools.back()
            no_ex = 0
        except ElementClickInterceptedException:
            tools.log_error(f'({j},{i}): {exhibitor.name}')
        except (IndexError, TimeoutException):
            tools.log_error(f'({j},{i}): {exhibitor.name}')
            tools.back()
        except NoSuchElementException:
            j += 1
            i = 1
            no_ex += 1
        finally:
            tools.save_exhibitor(exhibitor)
            i += 1

        if no_ex == 4:
            break


