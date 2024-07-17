# coding: utf8

from selenium import webdriver

browser = webdriver.Chrome()
browser.get("https://intergem.de/liste/?wpbdp_view=all_listings")

file = open('intergem_2020.txt', 'w')
file.write('Name\tStraße\tPLZ\tOrt\tLand\tTelefon\tFax\tE-Mail\tWeb\n')



file.close()
browser.quit()

# #wpbdp-listing-352 > div.listing-title > h2
# #wpbdp-listing-2815 > div.listing-title > h2

