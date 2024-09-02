from selenium.common.exceptions import TimeoutException

from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor

exhibitor_list_link = "https://www.new-housing.de/de/ausstellerliste/#/"
tools = Tools(RunMode.RUN)


def accept_cookies():
    input("DONE?????????")

def get_exhibitor_links():
    links = tools.get_saved_links()
    if len(links) != 0:
        return links

    tools.scroll()

    filter_str = '#/aussteller-detail/'
    links = tools.find_links(filter_str=filter_str)
    prefix = r'https://www.new-housing.de/de/ausstellerliste/'
    links = [prefix + l for l in links]

    tools.save_links(links)
    return links


def parse_exhibitor(ex: Exhibitor):
    css_name = '#app > div > div:nth-child(1) > div:nth-child(2) > div.col-xs-12.col-sm-8 > h1'
    css_street = '#app > div > div:nth-child(1) > div:nth-child(2) > div.col-xs-12.col-sm-8 > div > ul > li:nth-child(2) > h4'
    css_postcode = '#app > div > div:nth-child(1) > div:nth-child(2) > div.col-xs-12.col-sm-8 > div > ul > li:nth-child(1) > h3 > span:nth-child(1)'
    css_city = '#app > div > div:nth-child(1) > div:nth-child(2) > div.col-xs-12.col-sm-8 > div > ul > li:nth-child(1) > h3 > span:nth-child(2)'
    css_country = '#app > div > div:nth-child(1) > div:nth-child(2) > div.col-xs-12.col-sm-8 > div > ul > li:nth-child(1) > h3 > span:nth-child(3)'
    css_url = '#app > div > div:nth-child(1) > div:nth-child(2) > div.col-xs-12.col-sm-8 > div > ul > li:nth-child(5) > a'
    css_info = ''  
    css_tel = '#app > div > div:nth-child(1) > div:nth-child(2) > div.col-xs-12.col-sm-8 > div > ul > li:nth-child(3) > a'
    css_mail = '#app > div > div:nth-child(1) > div:nth-child(2) > div.col-xs-12.col-sm-8 > div > ul > li:nth-child(4) > a'
    css_fax = '#app > div > div:nth-child(1) > div:nth-child(2) > div.col-xs-12.col-sm-8 > div > ul > li:nth-child(6) > a'

    ex.name = tools.get_information_from_css_link(css_name)


    ex.street = tools.get_information_from_css_link(css_street, timeout=0.5)
    ex.postcode = tools.get_information_from_css_link(css_postcode, timeout=0.5).replace("-", '')
    ex.city = tools.get_information_from_css_link(css_city, timeout=0.5).replace(',','')
    ex.country = tools.get_information_from_css_link(css_country, timeout=0.5)


    data_css = [css_url, css_tel, css_fax, css_mail]
    for css in data_css:
        ex.sort_string(tools.get_information_from_css_link(css, timeout=0.5))

    info = tools.get_information_from_css_link(css_info, timeout=0.5)

    ex.add_info(info)

    if tools.run_mode == RunMode.TESTING:
        print(str(ex))


if __name__ == "__main__":
    tools.open_link(exhibitor_list_link)
    accept_cookies()
    links = get_exhibitor_links()
    for link in links:
        exhibitor: Exhibitor = Exhibitor()
        try:
            tools.open_link(link)
            parse_exhibitor(exhibitor)
            tools.back()
        except TimeoutException:
            tools.log_error(link)
        finally:
            tools.save_exhibitor(exhibitor)
