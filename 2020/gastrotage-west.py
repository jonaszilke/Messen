# coding: utf8

from selenium import webdriver
import ToolsMesse

browser = webdriver.Firefox()
browser.get("http://www.gastrotage-west.de/ausstellerliste-2020.html?L=0")

file = open('gastrotage-west.txt', 'w')
file.write('Name\tStraße\tPLZ\tOrt\tLand\tTelefon\tFax\tE-Mail\tWeb\n')


exhibitor = []

for i in range(48900, 49100):
    all_Data = ToolsMesse.getinformationfromcsslink(browser, "#c" + str(i) + " > div > div.innertext > p:nth-child(2)") \
        .replace("(at)", "@").replace("•", "\n").replace("Telefon ", "").replace("Fax ", "").replace("Mobil ", "")
    print(all_Data)

    if not all_Data.find("Italien") == -1:
        all_Data = ""
    if not all_Data.find("Schweiz") == -1:
        all_Data = ""
    if not all_Data.find("Österreich") == -1:
        all_Data = ""

    if not all_Data == "":
        data_array = all_Data.splitlines()
        if len(data_array) > 3:
            if ToolsMesse.find_place(data_array) != 2:
                data_array.pop(1)
            data_array = ToolsMesse.splitadresse(data_array)
            ToolsMesse.writeinfile(file, data_array, 4)
            exhibitor.append(i)

for i in exhibitor:
    print(str(i), end=", ")

# #c48982 > div > div.innertext > p:nth-child(2)

# #c49058 > div > div.innertext > p:nth-child(2)

# #c49042 > div > div.innertext > p:nth-child(2)

file.close()
browser.quit()

