from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

tools = Tools(RunMode.TESTING)


def accept_cookies():
    input("Please accept Cookies manually. Press 'ENTER' to continue!")


def get_exhibitor_links():
    # tools.scroll()
    wait = WebDriverWait(tools.driver, 10)

    # Wait for the elements to be present
    elems = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "h3")))
    for elem in elems:

        # Scroll the element into view
        tools.driver.execute_script("arguments[0].scrollIntoView();", elem)

        # Wait for the element to be clickable
        clickable_elem = wait.until(EC.element_to_be_clickable((By.TAG_NAME, "h3")))

        # Click the element
        clickable_elem.click()
        input("testetsettsett")

    links = tools.find_links()
    print(links)
    return links


def parse_exhibitor():
    css_name = ''
    css_street = ''
    css_postcode = ''
    css_city = ''
    css_tel = ''
    css_fax = ''
    css_url = ''
    css_info = ''

    exhibitor = Exhibitor()
    exhibitor.name = tools.get_information_from_css_link(css_name)
    exhibitor.street = tools.get_information_from_css_link(css_street)
    exhibitor.postcode = tools.get_information_from_css_link(css_postcode)
    exhibitor.city = tools.get_information_from_css_link(css_city)
    exhibitor.tel = tools.get_information_from_css_link(css_tel)
    exhibitor.fax = tools.get_information_from_css_link(css_fax)
    exhibitor.url = tools.get_information_from_css_link(css_url)
    exhibitor.info = tools.get_information_from_css_link(css_info)
    return exhibitor


if __name__ == '__main__':
    tools.open_link("https://www.messe-stuttgart.de/castforge/besucher/ausstellerverzeichnis#/")
    accept_cookies()
    links = get_exhibitor_links()
    for link in links:
        tools.open_link(link)
        exhibitor: Exhibitor = parse_exhibitor()
        tools.file.write(str(exhibitor))
        print(exhibitor.name)


##ed-list > div.ed-characterGroupWrapper > div.ed-characterGroup.clr > div:nth-child(2) > div > div > div.ed-grid > div.ed-grid__item.ed-grid__item--2 > div > h3
##ed-list > div.ed-characterGroupWrapper > div.ed-characterGroup.clr > div:nth-child(3) > div > div > div.ed-grid > div.ed-grid__item.ed-grid__item--2 > div > h3
##ed-list > div.ed-characterGroupWrapper > div.ed-characterGroup.clr > div:nth-child(4) > div > div > div.ed-grid > div.ed-grid__item.ed-grid__item--2 > div > h3
##ed-list > div.ed-characterGroupWrapper > div:nth-child(26) > div:nth-child(11) > div > div > div.ed-grid > div.ed-grid__item.ed-grid__item--2 > div > h3
