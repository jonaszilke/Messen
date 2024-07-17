# coding: utf8

from selenium import webdriver
from tools import ToolsMesse

timeout = 20
links = []

browser = webdriver.Firefox()

file = open('Bst.vds.txt', 'w')
file.write('Name\tStraße\tPLZ\tOrt\tLand\tTelefon\tFax\tMail\tWeb\n')

browser.get("https://bst.vds.de/messe-info/ausstellerverzeichnis/")

ToolsMesse.click_css_link(browser, "div.col-md-3:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > ul:nth-child(1) > li:nth-child(1) > ul:nth-child(2) > li:nth-child(1) > a:nth-child(1)")


def main_function():
    for i in range(2,115):
        x = []
        x.append(ToolsMesse.getinformationfromcsslink(browser, "div.panel:nth-child(" + str(i) + ") > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > h3:nth-child(2)"))
        for j in [1,2]:
            x.append(ToolsMesse.getinformationfromcsslink(browser, "div.panel:nth-child(" + str(i) + ") > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > ul:nth-child(3) > li:nth-child(" + str(j) + ")"))
        x.append(browser.find_element_by_css_selector("div.panel:nth-child("+str(i)+") > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > ul:nth-child(3) > li:nth-child(4) > a:nth-child(2)").get_attribute("href"))
        while '' in x:
            x.remove('')
        print(x)
        print("\n")
        ToolsMesse.writeinfile(file, x, 1)





main_function()

browser.quit()
file.close()

"""
div.panel:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2)
div.panel:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2)
div.panel:nth-child(4) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2)
div.panel:nth-child(114) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2)

name
div.panel:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > h3:nth-child(2)
tel
div.panel:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > ul:nth-child(3) > li:nth-child(1)
fax
div.panel:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > ul:nth-child(3) > li:nth-child(2)
web
div.panel:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > ul:nth-child(3) > li:nth-child(4)

"""