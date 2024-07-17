# coding: utf8

from selenium import webdriver
import ToolsMesse


browser = webdriver.Chrome()
browser.get("https://welovetravel.berlin/de/aussteller/")

file = open('welovetravel.txt', 'w')
file.write('Name\tStraße\tPLZ\tOrt\tLand\tTelefon\tFax\tE-Mail\tWeb\n')


def get_links_from_list():
    all_links = ToolsMesse.findlinksonpage(browser, "https://welovetravel.berlin/de/exhibitor/")
    for link in all_links:
        print(link)
    print(len(all_links))
    return all_links


def exhibitor():
    css_name = "#main > div > section > div > div > div.col-12.col-lg-8.single-exhbitor-main-section-body > h1"
    css_mail_web = "#main > div > section > div > div > div.col-lg-4.single-speaker-main-section-sidebar > " \
               "div.sticky-top.sticky-offset > " \
               "div.exhibitor-contact-container.knockout.bottom_30.d-flex.flex-column.align-items-center.align-items" \
               "-lg-start "

    data = ToolsMesse.getinformationfromcsslink(browser, css_mail_web).splitlines()
    data[0] = ToolsMesse.getinformationfromcsslink(browser, css_name)
    ToolsMesse.writeinfile(file, data, 1)


def ___main___():
    links = get_links_from_list()
    for link in links:
        browser.get(link)
        exhibitor()


___main___()

file.close()
browser.quit()
