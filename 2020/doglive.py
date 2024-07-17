# coding: utf8

from selenium import webdriver
from tools import ToolsMesse

timeout = 20

browser = webdriver.Firefox()

file = open('Doglive.txt', 'w')
file.write('Name\tStraße\tPLZ\tOrt\tLand\tTelefon\tFax\tMail\tWeb\n')

browser.get("https://www.doglive.de/de/besucher/ausstellerliste/")

# Cokies
ToolsMesse.click_css_link(browser, '.confirm-cookies')


def main_function():
    # Buchstabe
    for i in range(2, 26):
        # "div.hide-show-wrapper:nth-child("+str(i)+") > div:nth-child(2) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2)"
        finished = False
        j = 1
        while not finished:
            finished = exhibitor(i, j)
            j += 1


def exhibitor(i, j):
    #name
    name_link = "div.hide-show-wrapper:nth-child(" + str(i) +\
           ") > div:nth-child(2) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(" + str(j) +\
           ") > td:nth-child(2)"
    adresse_link = "div.hide-show-wrapper:nth-child(" + str(i) +\
           ") > div:nth-child(2) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(" + str(j) +\
           ") > td:nth-child(3)"
    name = ToolsMesse.getinformationfromcsslink(browser, name_link)
    adresse = ToolsMesse.getinformationfromcsslink(browser, adresse_link).splitlines()
    if name == "":
        return True
    data = [name]
    for ad in adresse:
        x = ad
        x = x.replace("Web: ", "").replace("E-Mail: ", "")
        data.append(x)
    if (data[-1].find("@") != -1) and (data[-2].find("www") != -1):
        x = data[-2]
        data[-2] = data[-1]
        data[-1] = x
        pass
    data = ToolsMesse.splitadresse(data)
    print(data)
    ToolsMesse.writeinfile(file, data, 4)
    return False


main_function()

browser.quit()
file.close()

# div.hide-show-wrapper:nth-child(2) > div:nth-child(2) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2)
# div.hide-show-wrapper:nth-child(2) > div:nth-child(2) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(2) > td:nth-child(2)
# div.hide-show-wrapper:nth-child(2) > div:nth-child(2) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(3) > td:nth-child(2)
# div.hide-show-wrapper:nth-child(3) > div:nth-child(2) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2)
# div.hide-show-wrapper:nth-child(25) > div:nth-child(2) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(8) > td:nth-child(2)

# div.hide-show-wrapper:nth-child(2) > div:nth-child(2) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(3)