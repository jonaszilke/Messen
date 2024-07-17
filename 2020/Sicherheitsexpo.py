# coding: utf8

from selenium import webdriver
import ToolsMesse
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import re

timeout = 1

browser = webdriver.Chrome()
browser.get("https://www.personal-world.de/aussteller/ausstellerliste/")

file = open('personalmesse.txt', 'w')
file.write('Name\tStraße\tPLZ\tOrt\tLand\tTelefon\tFax\tE-Mail\tWeb\n')

time.sleep(10)

links = ToolsMesse.findlinksonpage(browser, "www")

print(links)
print(len(links))

for link in links:
    file.write("\t"+link+"\n")

file.close()
browser.close()

# #c4154 > div > div.ce-bodytext > p:nth-child(1) > a
# #c4176 > div > div.ce-bodytext > p:nth-child(1) > a
# #c4161 > div > div.ce-bodytext > p:nth-child(1) > a
# #c116 > div > div.ce-bodytext > p > a
# #c122 > div > div.ce-bodytext > p > a
#
# #c3181 > div > div.ce-bodytext > p:nth-child(1) > a
# #c3314 > div > div.ce-bodytext > p:nth-child(1) > a
#c3859 > div > div.ce-bodytext > p:nth-child(1) > a
#
# [4154, 4156, 4157, 4158, 4159, 4160, 4161, 4162, 4163, 4164, 4166, 4169,
# 4175, 4176, 4179, 4186, 4213, 4225, 4226, 4228, 4230, 4231, 4234, 4235, 4237, 4238, 4243, 4244, 4252, 4253, 4254,
# 4255, 4257, 4258, 4261, 4262, 4263, 4283, 4284, 4285, 4293, 4300, 4301, 4302, 4303]
#
# [90, 116, 122, 125, 127, 129, 133, 137, 138, 140, 143, 146, 159, 160, 161, 162, 166, 178, 181, 187]
