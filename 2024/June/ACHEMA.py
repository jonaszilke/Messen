import time

from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException, TimeoutException

import ToolsMesse
from exhibitor import Exhibitor
from selenium import webdriver

name = "achema"
browser = webdriver.Chrome()
browser.get("https://www.achema.de/de/suche")

file = open(f'{name}.txt', 'w', encoding='utf-8')
file.write('Name\tStraße\tPLZ\tOrt\tLand\tTelefon\tFax\tE-Mail\tUrl\tInfo\n')


def accept_cookies():
    ToolsMesse.click_css_link(browser,
                              'body > div.cc-window.cc-banner.cc-type-opt-out.cc-theme-basic.cc-bottom.cc-color-override-1385250854 > div > div.cc-compliance.cc-highlight > a.cc-btn.cc-all')
    ToolsMesse.click_css_link(browser, '#ix-btn-list')
    ToolsMesse.click_css_link(browser, '#ix-selectOptions > div.select-page-container.col-12.col-sm-6 > div > span')
    ToolsMesse.click_css_link(browser,
                              '#ix-selectOptions > div.select-page-container.col-12.col-sm-6 > div > ul > li:nth-child(4)')

    ToolsMesse.click_css_link(browser, '#ix-filters > div > div.card-header > h2 > button > i')
    ToolsMesse.click_css_link(browser, '#ix-search-filter > div:nth-child(1) > div.form-group.col-12.col-md-5 > div')
    ToolsMesse.click_css_link(browser,
                              '#ix-search-filter > div:nth-child(1) > div.form-group.col-12.col-md-5 > div > ul > li:nth-child(11)')
    ToolsMesse.click_css_link(browser, '#ix-filters > div > div.card-header > h2 > button > i')
    time.sleep(5)

def get_exhibitor_links():
    links = []
    while True:
        try:
            ToolsMesse.click_css_link(browser, '#pagination > li.page-item.next')
            links += ToolsMesse.findlinksonpage(browser, filter='https://www.achema.de/de/aussteller/')
        except ElementNotInteractableException:
            break
    return links




def parse_exhibitor():
    exhibitor = Exhibitor()
    exhibitor.info = ToolsMesse.getinformationfromcsslink(browser, '#ix-aussteller-firm > div.col-12.col-sm-8.firma-name-container.d-flex.flex-column.justify-content-around > div.ix-text', True)

    # expand contact
    ToolsMesse.click_css_link(browser, '#ix-aussteller-contact > header > h2')
    data = []
    i = 1
    while True:
        try:
            d = ToolsMesse.getinformationfromcsslink(browser, f'#ix-aussteller-address > div:nth-child({i})', True, special_timeout=1)
            data.append(d)
            i += 1
        except TimeoutException:
            break

    exhibitor.name = data[0]
    try:
        country_index = data.index('Deutschland')
    except ValueError:
        print(f"Country not found: {exhibitor.name}")
        return
    exhibitor.street = data[country_index - 2]
    exhibitor.split_save_code_city(data[country_index-1])
    exhibitor.country = data[country_index]

    for d in data:
        if d[:5] == "Tel.:":
            exhibitor.tel = d[5:]
        elif d[:7] == "E-Mail:":
            exhibitor.mail = d[7:]
        elif d[:9] == "Internet:":
            exhibitor.url = d[9:]
        elif d[:4] == "Fax:":
            exhibitor.fax = d[4:]
    return exhibitor


def main_function():
    accept_cookies()
    links = get_exhibitor_links()
    for link in links:
        try:
            browser.get(link)
            exhibitor: Exhibitor = parse_exhibitor()
            file.write(str(exhibitor))
        except TimeoutException as e:
            print(e.stacktrace)
            with open(name+"_exceptions.txt", "a") as f:
                f.write(link+"\n")

main_function()

file.close()
browser.quit()
