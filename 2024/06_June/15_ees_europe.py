import os

from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor

exhibitor_list_link = "https://www.ees-europe.com/ausstellerliste"
tools = Tools(RunMode.RUN)


def accept_cookies():
    input('Accept Cookies')


def get_exhibitor_links():
    file_path = r'data/ees_exhibitor_links.txt'
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
    css_url = 'body > div.content.content-detail.content-detail-exhibitor > div.content-detail-related > div > div:nth-child(4) > dl > dt:nth-child(5)'
    css_info = 'body > div.content.content-detail.content-detail-exhibitor > div.content-detail-related > div > div:nth-child(2)'
    css_address = 'body > div.content.content-detail.content-detail-exhibitor > div.content-detail-related > div > div:nth-child(4) > dl > dt:nth-child(7)'
    css_tel = 'body > div.content.content-detail.content-detail-exhibitor > div.content-detail-related > div > div:nth-child(4) > dl > dt:nth-child(1)'
    css_mail = 'body > div.content.content-detail.content-detail-exhibitor > div.content-detail-related > div > div:nth-child(4) > dl > dt:nth-child(3)'

    data = []

    ex.name = tools.get_information_from_css_link(css_name)

    data.append(tools.get_information_from_css_link(css_url))
    data.append(tools.get_information_from_css_link(css_tel))
    data.append(tools.get_information_from_css_link(css_mail))
    data.append(tools.get_information_from_css_link(css_fax))

    address_str = tools.get_information_from_css_link(css_address)
    data += address_str.splitlines()[1:-1]
    data += address_str.splitlines()[-1].split(',')
    for i in data:
        ex.sort_string(i)
        ex.add_info(i)


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
        except Exception:
            tools.log_error(link)
        finally:
            tools.save_exhibitor(exhibitor)
