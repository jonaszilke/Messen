# coding: utf8

from selenium import webdriver
from bs4 import BeautifulSoup
from tools import ToolsMesse

timeout = 20
links = []


browser = webdriver.Firefox()


file = open('Parks2Clean.txt', 'w')
file.write('Name\tStraße\tPLZ\tOrt\tLand\tTelefon\tFax\tMail\tWeb\n')

browser.get("https://www.parts2clean.de/de/ausstellung/aussteller-produkte/ausstellerverzeichnisse/ausstellergesamtliste-a-z.xhtml")

print("Nach deutschen Austellernfiltern und auf Liste stellen")
inp = input("Fertig?")


def main_function():
    ToolsMesse.scroll(browser)
    raw_links = ToolsMesse.findlinksonpage(browser, "/aussteller/")
    for l in raw_links:
        links.append("https://www.parts2clean.de" + l)
    for l in links:
        print(l)
    print(len(links))

    for l in links:
        browser.get(l)
        exhibitor()


def exhibitor():
    # print(ToolsMesse.getinformationfromcsslink(browser, ".M03704 > div:nth-child(1)") + "\n\n\n")
    data = []
    data.append(ToolsMesse.findtextfromitemprop(browser, 'companyName').replace("\t", "")
                .replace("\n", "").replace("</h3>", "").replace('<h3 class="f-default" itemprop="companyName">', "")
                .replace("<br/>", " "))
    data.append(ToolsMesse.findtextfromitemprop(browser, 'street').replace("\t", "")
                .replace("\n", "").replace("</span>", "").replace('<span itemprop="street">', ""))
    data.append(ToolsMesse.findtextfromitemprop(browser, 'zip').replace("\t", "")
                .replace("\n", "").replace("</span>", "").replace('<span itemprop="zip">', ""))
    data.append(ToolsMesse.findtextfromitemprop(browser, 'country').replace("\t", "")
                .replace("\n", "").replace("</span>", "").replace('<span itemprop="country">', ""))
    tel = ToolsMesse.findtextfromitemprop(browser, 'phone')
    data.append(datafromstrring(tel, "tel:"))
    data.append(ToolsMesse.findtextfromitemprop(browser, 'fax').replace("\t", "")
                .replace("\n", "").replace("</span>", "").replace('<span itemprop="fax">', "").replace("Fax: ", "")
                .replace("None", ""))

    data.append(website())

    data = ToolsMesse.splitadresse(data)
    ToolsMesse.writeinfile(file, data)
    print(data[0])


def datafromstrring(string, replacement):
    soup = BeautifulSoup(string, "lxml")
    a = soup.find("a")
    try:
        return a["href"].replace(replacement, "")
    except TypeError:
        return ""


def website():

    text = []
    source_data = browser.page_source

    # Throw your source into BeautifulSoup and start parsing!
    soup = BeautifulSoup(source_data, "lxml")

    a = soup.find(class_="textLink icon-external-link", itemprop="url")
    try:
        return str(a['href'])
    except TypeError:
        return ""

main_function()

browser.close()
file.close()

"""
<a href="http://www.abnmetal.com" target="_blank" itemprop="url" class="textLink icon-external-link">Zur Unternehmenswebsite</a>

div.l-col4:nth-child(1) > div:nth-child(1) > h3:nth-child(1)
div.l-col4:nth-child(1) > div:nth-child(1) > h3:nth-child(1)
/html/body/div[1]/div/main/form/section[5]/div[2]/div[2]/section/div/div/div[1]/div/h3

"""