import time

from selenium.common.exceptions import TimeoutException

from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor

exhibitor_list_link = "https://dvet.by-qb.com/list/"
tools = Tools(RunMode.RUN)


def parse_exhibitor(ex: Exhibitor):
    css_name = '#exhibitorListDetail > h2'
    css_street = '#exhibitorListDetail > section.info > div:nth-child(2) > p:nth-child(1)'
    css_postcode = '#exhibitorListDetail > section.info > div:nth-child(2) > p:nth-child(2) > span:nth-child(1)'
    css_city = '#exhibitorListDetail > section.info > div:nth-child(2) > p:nth-child(2) > span:nth-child(2)'
    css_url = '#exhibitorListDetail > section.box.contact > span:nth-child(3) > span:nth-child(2)'
    css_tel = '#exhibitorListDetail > section.box.contact > span:nth-child(1) > span:nth-child(2)'
    css_fax = '#exhibitorListDetail > section.box.contact > span:nth-child(2) > span:nth-child(2)'
    time.sleep(1)
    ex.name = tools.get_information_from_css_link(css_name)
    ex.url = tools.get_information_from_css_link(css_url)
    ex.tel = tools.get_information_from_css_link(css_tel)
    ex.fax = tools.get_information_from_css_link(css_fax)

    ex.street = tools.get_information_from_css_link(css_street)
    ex.postcode = tools.get_information_from_css_link(css_postcode)
    ex.city = tools.get_information_from_css_link(css_city)

    if tools.run_mode == RunMode.TESTING:
        print(str(ex))


if __name__ == "__main__":
    tools.open_link(exhibitor_list_link)
    num_pages = 5
    exhibitor_per_page = 20
    for _ in range(num_pages):
        for i in range(exhibitor_per_page):
            css_exhibitor = f'#exhibitorListStart > section.main > ul > li:nth-child({i + 1}) > h3'
            exhibitor: Exhibitor = Exhibitor()
            try:
                time.sleep(1)
                tools.click_css_link(css_exhibitor)
                parse_exhibitor(exhibitor)
                tools.back()
            except TimeoutException:
                tools.log_error(exhibitor.name)
            finally:
                tools.save_exhibitor(exhibitor)
        time.sleep(1)
        css_next_page = '#exhibitorListStart > section.main > nav:nth-child(1) > i.btn-next.fa.fa-arrow-circle-o-right.fa-2x'
        tools.click_css_link(css_next_page)
