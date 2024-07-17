# coding: utf8

import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re

timeout = 20
links = []


browser = webdriver.Firefox()


file = open('Intergem.txt', 'w')
file.write('Name\tStraße\tPLZ\tOrt\tLand\tTelefon\tFax\tE-Mail\tWeb\n')


def findlinksonpage(link):

    browser.get(link)
    time.sleep(5)

    source_data = browser.page_source

    # Throw your source into BeautifulSoup and start parsing!
    soup = BeautifulSoup(source_data, "lxml")
    boolean = True

    for a in soup.find_all("a", href=re.compile("https://intergem.de/liste/")):
        if (a['href'][26:29].isdigit() ):
            if boolean:
                #print(a['href'])
                links.append(a['href'])
                print(a['href'])
                boolean = False
            else:
                boolean = True

    print(str(links.__len__()) + "\n\n")


for i in range(1, 8):
    print(i)
    #findlinksonpage("https://intergem.de/liste/page/"+str(i)+"/?wpbdp_view=all_listings#wpbdp-listings-list")
    findlinksonpage("https://intergem.de/liste/page/"+str(i)+"/?dosrch=1&q&wpbdp_view=search&listingfields%5B1%5D&listingfields%5B17%5D&listingfields%5B14%5D&listingfields%5B2%5D=-1&listingfields%5B12%5D%5B0%5D&listingfields%5B10%5D&listingfields%5B11%5D&listingfields%5B16%5D&listingfields%5B19%5D=Deutschland&listingfields%5B6%5D&listingfields%5B18%5D&listingfields%5B7%5D&listingfields%5B5%5D#wpbdp-listings-list")


def mainfunction():
    x = 1
    for c in links:
        browser.get(c)
        time.sleep(3)
        exhibitor()
        print(x)
        x = x+1


def exhibitor():
    print(getinformationfromcsslink(".listing-title > h2:nth-child(1)"))
    file.write(getinformationfromcsslink(".listing-title > h2:nth-child(1)") + "\t")
    complete_text_splitted = getinformationfromcsslink(".listing-details").splitlines()
    #print(complete_text_splitted)
    index = complete_text_splitted.index("Deutschland")
    text_needed = []
    if index is not -1:
        text_needed = complete_text_splitted[index-3:]
    writeinfile(text_needed)
    file.write("\n")


def writeinfile(data):
    n = 0
    try:
        file.write(data[0] + "\t")
        file.write(data[1][-5:] + "\t")
        file.write(data[2] + "\t")
        file.write(data[3] + "\t")
        if not (data[4].find("Tel") == -1):
            file.write(data[4][6:])
            n = n-1
        file.write("\t")
        n = n+1
        if not (data[5-n].find("Fax") == -1):
            file.write(data[5-n][5:])
            n = n-1
        file.write("\t")
        n = n + 1
        if not (data[6-n].find("E-Mail") == -1):
            file.write(data[6-n][8:])
            n = n - 1
        n = n + 1
        file.write("\t")
        if not (data[7 - n].find("Internet") == -1):
            file.write(data[7 - n][10:])
    except IndexError:
        print("Array out of range")





def getinformationfromcsslink(csslink):
    try:

        element_present = EC.presence_of_element_located((By.CSS_SELECTOR, csslink))
        WebDriverWait(browser, timeout).until(element_present)
        return browser.find_element_by_css_selector(csslink).text
    except TimeoutException as e:
        print("TIMEOUT")
    except NoSuchElementException as e:
        print("NO_SUCH_ELEMENT")
    return ""


mainfunction()

browser.quit()
