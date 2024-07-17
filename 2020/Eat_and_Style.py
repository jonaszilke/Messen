# coding: utf8

import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from tools import ToolsMesse

timeout = 20
links = []

browser = webdriver.Firefox()

file = open('Eat_and_Style.txt', 'w')
file.write('Name\tStraße\tPLZ\tOrt\tLand\tTelefon\tFax\tMail\tWeb\n')

browser.get("https://www.eat-and-style.de/stuttgart/aussteller/")

ToolsMesse.click_css_link(browser, 'p._brlbs-accept:nth-child(4) > a:nth-child(1)')

def main_function():
    finished = False
    while not finished:
        list()
        try:
            ToolsMesse.click_css_link(browser, '.next')
            time.sleep(2)
        except(TimeoutException):
            finished = True



def list():
    for i in range(1,26):
        ToolsMesse.click_css_link(browser, 'li.eat-and-style-exhibitor-list-content-results-item:nth-child(' + str(i) + ') > div:nth-child(1) > span:nth-child(3) > a:nth-child(1)')
        time.sleep(1)
        exhibitor()
        time.sleep(1)
        ToolsMesse.click_css_link(browser, '.eat-and-style-exhibitor-details-content-header > a:nth-child(2)')

def exhibitor():
    adress = ToolsMesse.getinformationfromcsslink(browser, '.eat-and-style-exhibitor-details-content-address-inner > address:nth-child(2)').splitlines()
    # print(name + "\t" + adress[0])
    # web = ToolsMesse.getinformationfromcsslink(browser, '.eat-and-style-exhibitor-details-content-contact-inner > span:nth-child(2) > a:nth-child(2)')
    # tel = ToolsMesse.getinformationfromcsslink(browser, '.eat-and-style-exhibitor-details-content-contact-inner > span:nth-child(3) > a:nth-child(2)')
    # mail = ToolsMesse.getinformationfromcsslink(browser, '.eat-and-style-exhibitor-details-content-contact-inner > span:nth-child(4) > a:nth-child(2)')

    # adress.append(tel)
    # adress.append(mail)
    # adress.append(web)

    temp = []

    adress2 = ToolsMesse.getinformationfromcsslink(browser, '.eat-and-style-exhibitor-details-content-contact-inner').splitlines()
    for i in adress2:
        if (i.find("facebook") == -1) and (i.find("instagram") == -1) and (i.find("Kontakt") == -1) and (not i == "http://"):
            temp.append(i)

    try:
        adress.append(temp[1])
        adress.append(temp[2])
    except IndexError:
        pass
    try:
        adress.append(temp[0])
    except IndexError:
        pass


    for i in adress:
        print(i)
    print()

    try:
        adress.index("Deutschland")
        ToolsMesse.writeinfile(file, adress)
        print('done')
        pass
    except ValueError:
        pass


main_function()

browser.quit()
file.close()

# .eat-and-style-exhibitor-details-content-address-inner > address:nth-child(2)
