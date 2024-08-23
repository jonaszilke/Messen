import os

from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor

prefix = "https://www.powertodrive.de"
exhibitor_list_link = prefix + "/ausstellerliste"
tools = Tools(RunMode.RUN)


def accept_cookies():
    input('Accept Cookies')


def get_exhibitor_links():
    links = tools.get_saved_links()
    if len(links) != 0:
        return links

    # Links not leaded yet
    input("Please scroll to the end of the site until all exhibitors are loaded")
    filter_str = '/ausstellerliste/'
    links = tools.find_links(filter_str=filter_str)
    links = [prefix + l for l in links]

    tools.save_links(links)
    return links


def parse_exhibitor(ex: Exhibitor):
    css_name = 'body > div.content.content-detail.content-detail-exhibitor > div.content-detail-main > div > div.content-data-headline > h1'
    css_url = 'body > div.content.content-detail.content-detail-exhibitor > div.content-detail-related > div > div:nth-child(4) > dl > dt:nth-child(5)'
    css_info = 'body > div.content.content-detail.content-detail-exhibitor > div.content-detail-related > div > div:nth-child(2)'
    css_address = 'body > div.content.content-detail.content-detail-exhibitor > div.content-detail-related > div > div:nth-child(4) > dl > dt:nth-child(7)'
    css_tel = 'body > div.content.content-detail.content-detail-exhibitor > div.content-detail-related > div > div:nth-child(4) > dl > dt:nth-child(1)'
    css_mail = 'body > div.content.content-detail.content-detail-exhibitor > div.content-detail-related > div > div:nth-child(4) > dl > dt:nth-child(3)'

    data = []

    ex.name = tools.get_information_from_css_link(css_name)

    data.append(tools.get_information_from_css_link(css_url, timeout=0.5))
    data.append(tools.get_information_from_css_link(css_tel, timeout=0.5))
    data.append(tools.get_information_from_css_link(css_mail, timeout=0.5))

    address_str = tools.get_information_from_css_link(css_address, timeout=0.5)
    data += address_str.splitlines()[1:-1]
    data += address_str.splitlines()[-1].split(',')
    for i in data:
        ex.sort_string(i)
        ex.add_info(i)


    info = tools.get_information_from_css_link(css_info, timeout=0.5)

    ex.add_info(info)

    if tools.run_mode == RunMode.TESTING:
        print(str(ex))


if __name__ == "__main__":
    tools.open_link(exhibitor_list_link)
    tools.driver.maximize_window()
    accept_cookies()
    links = get_exhibitor_links()
    for link in links:
        exhibitor: Exhibitor = Exhibitor()
        try:
            tools.open_link(link)
            parse_exhibitor(exhibitor)
        except Exception:
            tools.log_error(link)
        finally:
            tools.save_exhibitor(exhibitor)
