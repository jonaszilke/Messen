# coding: utf8

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

timeout = 20
back = True

file = open('cadeaux-leipzig.txt', 'w')
file.write('Name\tStraße\tPLZ\tOrt\tLand\tTelefon\tFax\tMail\tWebseite\n')

browser = webdriver.Firefox()
browser.get("https://www.cadeaux-leipzig.de/aussteller-produkte")

time.sleep(2)

cookie = EC.presence_of_element_located((By.CSS_SELECTOR, '#cookie-accept'))
WebDriverWait(browser, timeout).until(cookie)
browser.find_element_by_css_selector('#cookie-accept').click()
time.sleep(2)

print("Nach deutschen Aussteller filtern")
j = input("Fertig?  ")


def hauptfunktion():

    for i in range(1, 19):
        try:
            link = "div.result-pagination-bar:nth-child(4) > div:nth-child(2) > div:nth-child(1) > button:nth-child(3) > img:nth-child(1)"
            if(i == 1):
                link = "div.result-pagination-bar:nth-child(4) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)"
            print ("\n\n"+str(i))
            liste()
            element_present = EC.presence_of_element_located((By.CSS_SELECTOR, link))
            WebDriverWait(browser, timeout).until(element_present)
            browser.find_element_by_css_selector(link).click()
        except TimeoutException:
            print("Liste nicht gefunden: " + str(i))
        except NoSuchElementException:
            print("NoSuchElement")


def liste():
    global back
    for i in range(1, 11):
        try:
            #       #exhibitorsandproductstable > li:nth-child(4)
            link = "#exhibitorsandproductstable > li:nth-child("+str(i)+")"
            element_present = EC.presence_of_element_located((By.CSS_SELECTOR, link))
            WebDriverWait(browser, timeout).until(element_present)
            browser.find_element_by_css_selector(link).click()
            einzelnerAussteller()
            if back:
                browser.execute_script("window.history.go(-1)")
            else:
                back = True
        except TimeoutException:
            pass


def einzelnerAussteller():
    try:
        try:
            element_present = EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'div.floatl:nth-child(2) > div:nth-child(1) > h3:nth-child(1) > a:nth-child(1)'))
            WebDriverWait(browser, timeout).until(element_present)
        except TimeoutException:
            print('Timed out')


        time.sleep(2)
        # print(browser.find_element_by_css_selector('div.floatl:nth-child(2) > div:nth-child(1) > h3:nth-child(1) > a:nth-child(1)').text)
        # print('-----')
        # print(browser.find_element_by_css_selector('div.floatl:nth-child(2) > div:nth-child(1) > div:nth-child(2)').text)
        # print('-----')
        # print(browser.find_element_by_css_selector('div.floatl:nth-child(2) > div:nth-child(1)').text)
        # print('-----')
        s1 = browser.find_element_by_css_selector('div.floatl:nth-child(2) > div:nth-child(1)').text
        # print(s1)
        s2 = [s.strip() for s in s1.splitlines()]
        # print(len(s2[0]))
        print(s2[0])

        file.write(s2[0])
        file.write('\t')
        file.write(s2[1])
        file.write('\t')
        file.write(s2[2][:5])
        file.write('\t')
        file.write(s2[2][6:])
        file.write('\t')
        file.write(s2[3])
        file.write('\t')

        for k in range(4, len(s2)):
            if s2[k].find('Tel.:') >= 0:
                bla = s2[k].replace('Tel.:', '')
                file.write(bla.strip())
                continue

            if s2[k].find('Fax:') >= 0:
                bla = s2[k].replace('Fax:', '')
                if s2[k - 1].find('Tel.:') >= 0:
                    file.write('\t')
                else:
                    file.write('\t\t')
                file.write(bla.strip())
                continue

            if s2[k].find('Email:') >= 0:
                bla = s2[k].replace('Email:', '')
                if s2[k - 1].find('Fax:') >= 0:
                    file.write('\t')
                else:
                    file.write('\t\t')
                file.write(bla.strip())
                continue

            if s2[k].find('Internet:') >= 0:
                bla = s2[k].replace('Internet:', '')
                if s2[k - 1].find('Email:') >= 0:
                    file.write('\t')
                else:
                    file.write('\t\t\t')
                file.write(bla.strip())
                continue

        try:
            s3 = browser.find_element_by_css_selector('div.box700:nth-child(2) > p:nth-child(2)').text
            #file.write('\t')
            #file.write(s3)
        except NoSuchElementException:
            pass
    except NoSuchElementException:
        print("kein vernünftiger Aussteller")
        global back
        back = False
    except IndexError:
        pass

    file.write('\n')


hauptfunktion()

browser.quit()
file.close()

# #exhibitorsandproductstable > li:nth-child(10) > div.list-item-content.clearfix > div > h3 > a
