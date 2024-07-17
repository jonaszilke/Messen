from selenium.common.exceptions import TimeoutException

import ToolsMesse
from exhibitor import Exhibitor
from selenium import webdriver
import os

name = os.path.basename(__file__)[:-3]
browser = webdriver.Chrome()
browser.get("https://www.messe-stuttgart.de/castforge/besucher/ausstellerverzeichnis#/")

file = open(f'{name}.txt', 'w', encoding='utf-8')
file.write('Name\tStraße\tPLZ\tOrt\tLand\tTelefon\tFax\tE-Mail\tUrl\tInfo\n')


def accept_cookies():
    css_cookies = '#uc-center-container > div.sc-eBMEME.jAnYIK > div > div.sc-jsJBEP.bHqEwZ > div > button.sc-dcJsrY.hzfqX'
    test        = '#uc-center-container > div.sc-eBMEME.jAnYIK > div > div.sc-jsJBEP.bHqEwZ > div > div > button.sc-dcJsrY.iKkUUc'
    # ToolsMesse.click_css_link(browser, css_cookies, special_timeout=10)


def get_exhibitor_links():
    ToolsMesse.scroll(browser)
    links = ToolsMesse.findlinksonpage(browser, filter='/ausstellerliste/detail')
    links = ToolsMesse.findlinksonpage(browser)
    print(links)
    exit(0)
    return links


def parse_exhibitor():
    css_name = ''
    css_street = ''
    css_postcode = ''
    css_city = ''
    css_tel = ''
    css_fax = ''
    css_url = ''
    css_info = ''

    exhibitor = Exhibitor()
    exhibitor.name = ToolsMesse.getinformationfromcsslink(browser, css_name)
    exhibitor.street = ToolsMesse.getinformationfromcsslink(browser, css_street)
    exhibitor.postcode = ToolsMesse.getinformationfromcsslink(browser, css_postcode)
    exhibitor.city = ToolsMesse.getinformationfromcsslink(browser, css_city)
    exhibitor.tel = ToolsMesse.getinformationfromcsslink(browser, css_tel)
    exhibitor.fax = ToolsMesse.getinformationfromcsslink(browser, css_fax)
    exhibitor.url = ToolsMesse.getinformationfromcsslink(browser, css_url)
    exhibitor.info = ToolsMesse.getinformationfromcsslink(browser, css_info)
    return exhibitor


def main_function():
    accept_cookies()
    links = get_exhibitor_links()
    for link in links:
        try:
            browser.get(link)
            exhibitor: Exhibitor = parse_exhibitor()
            file.write(str(exhibitor))
            print(exhibitor.name)
        except TimeoutException as e:
            with open(name+"_exceptions.txt", "a") as f:
                f.write(link+"\n")

# #ed-list > div.ed-characterGroupWrapper > div:nth-child(1) > div:nth-child(2) > div > div > a
# #ed-list > div.ed-characterGroupWrapper > div:nth-child(1) > div:nth-child(3) > div > div > a
main_function()

file.close()
browser.quit()
