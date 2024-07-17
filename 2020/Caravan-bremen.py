# coding: utf8

import time
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import ToolsMesse

timeout = 20
links = []

browser = webdriver.Firefox()

file = open('Caravan-bremen.txt', 'w')
file.write('Name\tStraße\tPLZ\tOrt\tLand\tTelefon\tFax\tMail\tWeb\n')

browser.get(
    "https://www.caravan-bremen.de/cv_aussteller_de?content=suchergebnis&pagemode=results&design=infa&start_halle_search=start_halle_search&halle_suchbegriff=006&start_halle_search=Suche+starten#ExProContent")


def find_exhibitor_links():
    for i in range(5, 8):
        browser.get(
            "https://www.caravan-bremen.de/cv_aussteller_de?content=suchergebnis&pagemode=results&design=infa&start_halle_search=start_halle_search&halle_suchbegriff=00"+str(i)+"&start_halle_search=Suche+starten#ExProContent")
        time.sleep(2)
        links2 = ToolsMesse.findlinksonpage(browser, "content=suchergebnis&pagemode=results&suchanfrage=halle_suchbegriff=00")
        for l in links2:
            links.append("https://www.caravan-bremen.de/cv_aussteller_de" + l)
    for l in links:
        print(l)
    print(len(links))


def main_function():
    find_exhibitor_links()
    for l in links:
        browser.get(l)
        time.sleep(2)
        exhibitor()


def exhibitor():
    address = ToolsMesse.getinformationfromcsslink(browser, ".CompanyDetail > p:nth-child(4)").splitlines()

    while len(address)>4:
        address[0] = address[0] + address.pop(1)

    address = ToolsMesse.splitadresse(address, 2)
    further_information = ToolsMesse.getinformationfromcsslink(browser, ".CompanyDetail > p:nth-child(5)").splitlines()
    for s in range(0, len(further_information)):
        if not further_information[s].find("Tel") == -1:
            further_information[s] = further_information[s][6:]
        elif not further_information[s].find("Fax") == -1:
            further_information[s] = further_information[s][5:]
        elif not further_information[s].find("E-Mail") == -1:
            further_information[s] = further_information[s][8:]
        elif not further_information[s].find("Web") == -1:
            further_information[s] = further_information[s][5:]

    for s in further_information:
        address.append(s)
    print(address[0])

    ToolsMesse.writeinfile(file, address)


main_function()
browser.close()
file.close()
