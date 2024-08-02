from selenium.common.exceptions import TimeoutException

from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor

exhibitor_list_link = ''  # TODO
tools = Tools(RunMode.TESTING)


def accept_cookies():
    css_accept = ''  # TODO
    tools.click_css_link(css_accept)


def parse_exhibitor(ex: Exhibitor):
    css_name = ''  # TODO
    css_street = ''  # TODO
    css_postcode = ''  # TODO
    css_city = ''  # TODO
    css_country = ''  # TODO
    css_url = ''  # TODO
    css_info = ''  # TODO
    css_tel = ''  # TODO
    css_mail = ''  # TODO
    css_fax = ''  # TODO

    ex.name = tools.get_information_from_css_link(css_name)
    ex.url = tools.get_information_from_css_link(css_url)
    ex.tel = tools.get_information_from_css_link(css_tel)
    ex.mail = tools.get_information_from_css_link(css_mail)
    ex.fax = tools.get_information_from_css_link(css_fax)

    ex.street = tools.get_information_from_css_link(css_street)
    ex.postcode = tools.get_information_from_css_link(css_postcode)
    ex.city = tools.get_information_from_css_link(css_city)
    ex.country = tools.get_information_from_css_link(css_country)

    info = tools.get_information_from_css_link(css_info)

    ex.add_info(info)

    if tools.run_mode == RunMode.TESTING:
        print(str(ex))


if __name__ == "__main__":
    tools.open_link(exhibitor_list_link)
    accept_cookies()

    num_pages = 1  # TODO
    exhibitor_per_page = 1  # TODO
    css_next_page = ''  # TODO
    for _ in range(num_pages):
        for i in range(exhibitor_per_page):
            css_exhibitor = f''  # TODO
            exhibitor: Exhibitor = Exhibitor()
            try:
                tools.click_css_link(css_exhibitor)
                parse_exhibitor(exhibitor)
                tools.back()
            except TimeoutException:
                tools.log_error(exhibitor.name)
            finally:
                tools.save_exhibitor(exhibitor)
        tools.click_css_link(css_next_page)
