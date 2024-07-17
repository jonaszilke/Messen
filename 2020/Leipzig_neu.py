# coding: utf8

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
import re
from tools import ToolsMesse

name = "cadeaux-leipzig"

browser = webdriver.Firefox()
browser.get(f"https://www.{name}.de/aussteller-produkte")

file = open(f'{name}.txt', 'w')
file.write('Name\tStraße\tPLZ\tOrt\tLand\tTelefon\tFax\tE-Mail\tWeb\n')


links = []


def filter_exhibitor():
    ToolsMesse.click_css_link(browser, ".icon-plus")
    select = Select(browser.find_element_by_css_selector("#country"))
    select.select_by_visible_text("Bundesrepublik Deutschland")

    ToolsMesse.click_css_link(browser, "#selectedFilter2")
    ToolsMesse.click_css_link(browser, ".main-search-input > button:nth-child(2)")
    ToolsMesse.click_css_link(browser, ".icon-minus")


def get_links_from_list():
    all_links = ToolsMesse.findlinksonpage(browser, "/aussteller-produkte/aussteller/")
    for l in all_links:
        if bool(re.match('/aussteller-produkte/aussteller/.*/[0-9]{6}$', l)):
            global links
            links.append(f"https://www.{name}.de"+l)


def get_all_links():
    try:
        i = 1
        while True:
            link = "div.result-pagination-bar:nth-child(4) > div:nth-child(2) > div:nth-child(1) > button:nth-child(3) > img:nth-child(1)"
            if i == 1:
                link = "div.result-pagination-bar:nth-child(4) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)"
            i += 1
            get_links_from_list()
            ToolsMesse.click_css_link(browser, link)
    except TimeoutException:
        print(len(links))
        pass


def main_function():
    filter_exhibitor()
    get_all_links()
    global links

    for l in links:
        browser.get(l)
        exhibitor()


def exhibitor():
    try:
        data = ToolsMesse.getinformationfromcsslink(browser, "div.floatl:nth-child(2) > div:nth-child(1)", True).\
            replace("Tel.: ", "").replace("Fax: ", "").replace("Email: ", "").replace("Internet: ", "").splitlines()
        data = ToolsMesse.splitadresse(data)
        ToolsMesse.writeinfile(file, data)
    except TimeoutException:
        pass


main_function()

file.close()
browser.quit()
