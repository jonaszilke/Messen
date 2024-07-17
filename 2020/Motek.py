# coding: utf8

import time
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import ToolsMesse

timeout = 20
links = []


browser = webdriver.Firefox()


file = open('Motek2.txt', 'w')
file.write('Name\tStraße\tPLZ\tOrt\tLand\tTelefon\tFax\tE-Mail\tWeb\n')

browser.get("https://www.motek-messe.de/ausstellerverzeichnis/")

counter = 0

print("Nach deutschen Austellernfiltern")
inp = input("Fertig?")


def scroll():
    lenOfPage = browser.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match = False
    while (match == False):
        lastCount = lenOfPage
        time.sleep(3)
        lenOfPage = browser.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        if lastCount == lenOfPage:
            match = True


def findlinksonpage():
    global counter
    source_data = browser.page_source

    # Throw your source into BeautifulSoup and start parsing!
    soup = BeautifulSoup(source_data, "lxml")

    for a in soup.find_all("a", href=re.compile("https://www.motek-messe.de/ausstellerverzeichnis/showroom/")):
        links.append(a['href'])
        print(a['href'])
        counter = counter + 1


def mainfunction():
    scroll()
    findlinksonpage()
    print(counter)
    for l in links:
        browser.get(l)
        time.sleep(3)
        exhibitor()


def exhibitor():
    all = gifcssl(".mc-box-exh > div:nth-child(4)")

    # print("All: \n" +all )

    rawdata = all.splitlines()[1:]
    print(rawdata[0])
    index = rawdata.index("Deutschland")
    data = [rawdata[0]]
    data.extend(rawdata[index-2:])
    ToolsMesse.writeinfile(file, ToolsMesse.splitadresse(data))


def gifcssl(link):
    return ToolsMesse.getinformationfromcsslink(link, browser)


mainfunction()

browser.quit()
file.close()
