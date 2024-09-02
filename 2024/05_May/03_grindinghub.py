import time

from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor

exhibitor_list_link = "https://www.grindinghub.de/besucher/ausstellerverzeichnis#/exhibitor/"
tools = Tools(RunMode.RUN)


def accept_cookies():
    input('Accept Cookies!!')


def parse_exhibitor(ex: Exhibitor):
    css_info = 'div.ed-contacts'

    data = tools.get_information_from_css_link(css_info, throw_exception=True).splitlines()
    name = data[0]
    name_split = name.split('|')
    if len(name_split) == 2:
        ex.name = name_split[1].strip()
    else:
        ex.name = name


    for d in data[1:]:
        ex.sort_string(d)

    if tools.run_mode == RunMode.TESTING:
        print(str(ex))


if __name__ == "__main__":
    tools.open_link(exhibitor_list_link)
    tools.driver.maximize_window()
    accept_cookies()
    tools.scroll()
    tools.driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(3)
    i = 1
    j = 1
    no_ex = 0
    while True:

        exhibitor: Exhibitor = Exhibitor()
        try:
            css_link = f'#ed-list > div.ed-characterGroupWrapper > div:nth-child({j}) > div > div:nth-child({i}) > div > div:nth-child(3) > a'
            tools.scroll_css_into_view(css_link)
            time.sleep(0.5)
            tools.driver.execute_script("window.scrollBy(0, -100);")
            time.sleep(0.5)
            tools.click_css_link(css_link)
            parse_exhibitor(exhibitor)
            tools.back()
            no_ex = 0
        except ElementClickInterceptedException:
            tools.log_error(f'{i}: {exhibitor.name}')
        except (TimeoutException, IndexError):
            tools.log_error(f'{i}: {exhibitor.name}')
            tools.back()
        except NoSuchElementException:
            j += 1
            i = 0
            no_ex += 1
        finally:
            tools.save_exhibitor(exhibitor)
            i += 1

        if no_ex == 4:
            break


