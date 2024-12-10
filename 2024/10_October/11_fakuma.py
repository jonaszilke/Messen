import time

from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor

exhibitor_list_link = "https://www.fakuma-messe.de/ausstellerverzeichnis/"
tools = Tools(RunMode.RUN)


def accept_cookies():

    for i in range(10):
        try:
            css_accept = '#CookieBoxSaveButton'
            tools.click_css_link(css_accept, timeout=10)
            return
        except:
            print(i)
            tools.driver.refresh()


def get_exhibitor_links():
    links = []
    filter_str = 'https://www.fakuma-messe.de/Ausstellerverzeichnis/'
    prefix = ''
    i = 1
    while True:
        list_link = f'https://www.fakuma-messe.de/ausstellerverzeichnis/?pg={i}'
        tools.open_link(list_link)
        new_links = [prefix + l for l in tools.find_links(filter_str=filter_str)]
        if len(new_links) == 0:
            break
        links += new_links
        i += 1

    return links


def parse_exhibitor(ex: Exhibitor):
    css_all_info = 'div.profile-info'
    all_info = tools.get_information_from_css_link(css_all_info).splitlines()
    try:
        stop_index = all_info.index('Sales Kontakt')
        all_info = all_info[:stop_index]
    except ValueError:
        pass

    css_name = 'div.profile-info > h5'
    ex.name = tools.get_information_from_css_link(css_name).replace('\n', ' ')

    start_index = 0
    for i in range(len(all_info)):
        if all_info[i] not in ex.name:
            start_index = i
            break
    all_info = all_info[start_index:]
    ex.sort_list(all_info)


if __name__ == "__main__":
    tools.open_link(exhibitor_list_link)
    accept_cookies()
    links = tools.get_links(get_exhibitor_links)
    tools.iterate_exhibitor_links(links, parse_exhibitor)
