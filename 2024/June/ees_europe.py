import os
import time

from selenium.common.exceptions import TimeoutException

from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor

exhibitor_list_link = "https://www.ees-europe.com/ausstellerliste"
tools = Tools(RunMode.TESTING)


def accept_cookies():
    input('Accept Cookies')


def get_exhibitor_links():
    file_path = 'ees_exhibitor_links.txt'
    if os.path.exists(file_path):
        # If the file doesn't exist, create it
        with open(file_path, 'r') as file:
            return file.readlines()

    # Links not leaded yet
    input("Please scroll to the end of the site until all exhibitors are loaded")
    filter_str = '/ausstellerliste/'
    links = tools.find_links(filter_str=filter_str)
    prefix = 'https://www.ees-europe.com'
    links = [prefix + l for l in links]

    with open(file_path, 'w') as file:
        file.write('\n'.join(links))
    return links


def parse_exhibitor(ex: Exhibitor):
    css_name = 'body > div.content.content-detail.content-detail-exhibitor > div.content-detail-main > div > div.content-data-headline > h1'
    css_street = ''  # TODO
    css_postcode = ''  # TODO
    css_city = ''  # TODO
    css_country = ''  # TODO
    css_url = 'body > div.content.content-detail.content-detail-exhibitor > div.content-detail-related > div > div:nth-child(4) > dl > dt:nth-child(5)'
    css_info = 'body > div.content.content-detail.content-detail-exhibitor > div.content-detail-related > div > div:nth-child(4) > dl > dt:nth-child(7)'
    css_tel = 'body > div.content.content-detail.content-detail-exhibitor > div.content-detail-related > div > div:nth-child(4) > dl > dt:nth-child(1)'
    css_mail = 'body > div.content.content-detail.content-detail-exhibitor > div.content-detail-related > div > div:nth-child(4) > dl > dt:nth-child(3)'
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
    tools.driver.maximize_window()
    accept_cookies()
    links = get_exhibitor_links()
    for link in links:
        exhibitor: Exhibitor = Exhibitor()
        try:
            tools.open_link(link)
            parse_exhibitor(exhibitor)
        except TimeoutException:
            tools.log_error(link)
        finally:
            tools.save_exhibitor(exhibitor)
