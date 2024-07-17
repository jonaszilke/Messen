# coding: utf8

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import ToolsMesse


browser = webdriver.Chrome()
browser.get("https://www.provention-erfurt.de/aussteller/ausstellerliste-2020/")

file = open('provention-erfurt.txt', 'w')
file.write('Name\tStraße\tPLZ\tOrt\tLand\tTelefon\tFax\tE-Mail\tWeb\n')


def __main__():
    ToolsMesse.click_css_link(browser, "#uc-btn-accept-banner")
    try:
        for i in range(1, 9):
            list(i)
            ToolsMesse.click_css_link(browser, "#c5245 > div > div.exhibitors-pagination.pagination-top > nav > "
                                               "ul:nth-child(3) > li:nth-child(1) > a")
    except TimeoutException:
        pass


def list(page):
    for i in range(2, 20):
        ToolsMesse.click_css_link(browser, f"#c5245 > div > div.exhibitors-pagination.pagination-top > nav > "
                                           f"ul:nth-child(2) > li:nth-child({page}) > a")
        ToolsMesse.click_css_link(browser, f"#c5245 > div > div.exhibitors-list > div:nth-child({i}) > div.exhibitor"
                                           f"-header > p.exhibitor-title > a")
        exhibitor()
        browser.execute_script("window.history.go(-1)")


def exhibitor():
    data = []

    for i in [2, 4, 6, 8, 10]:
        data.append(ToolsMesse.getinformationfromcsslink(browser, f"#c5245 > div > div > div.exhibitor-facts > dl > dd:nth-child({i})"))
    for i in [2, 4, 6]:
        data.append(ToolsMesse.getinformationfromcsslink(browser, f"#c5245 > div > div > div.exhibitor-contact > dl > dd:nth-child({i})"))

    if data[4] == "Deutschland":
        ToolsMesse.writeinfile(file, data)


__main__()


file.close()
browser.quit()
