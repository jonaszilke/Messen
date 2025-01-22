import time

from selenium.common.exceptions import TimeoutException, NoSuchElementException

from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor

exhibitor_list_link = "https://digital.eurotier.com/newfront/marketplace/exhibitors?limit=12&pageNumber=1"
tools = Tools(RunMode.RUN)


def accept_cookies():
    css_accept = '#ccm-widget > div > div.ccm-modal--body > div.ccm-widget--buttons > button.button.ccm--save-settings.ccm--button-primary.ccm--ctrl-init'
    tools.click_css_link(css_accept)
    input('Filter for EnergyDecentral')


def get_exhibitor_links():
    links = []
    filter_str = '/newfront/exhibitor/'
    prefix = 'https://digital.eurotier.com'
    links += [prefix + l for l in tools.find_links(filter_str=filter_str)]
    return links


def parse_exhibitor(ex: Exhibitor):
    css_name = '#__next > div.MuiBox-root.css-g9qx4c > main > div > div > div > div.MuiGrid-root.MuiGrid-item.MuiGrid-grid-xs-12.MuiGrid-grid-md-6.MuiGrid-grid-lg-4.css-obamm2 > div > div > div:nth-child(1) > div > div.MuiBox-root.css-qexdkq > h2'
    css_street = '#__next > div.MuiBox-root.css-g9qx4c > main > div > div > div > div.MuiGrid-root.MuiGrid-item.MuiGrid-grid-xs-12.MuiGrid-grid-md-6.MuiGrid-grid-lg-4.css-obamm2 > div > div > div:nth-child(1) > div > div.MuiBox-root.css-1at62qq > p:nth-child(1)'
    css_city = '#__next > div.MuiBox-root.css-g9qx4c > main > div > div > div > div.MuiGrid-root.MuiGrid-item.MuiGrid-grid-xs-12.MuiGrid-grid-md-6.MuiGrid-grid-lg-4.css-obamm2 > div > div > div:nth-child(1) > div > div.MuiBox-root.css-1at62qq > p:nth-child(2)'
    css_country = '#__next > div.MuiBox-root.css-g9qx4c > main > div > div > div > div.MuiGrid-root.MuiGrid-item.MuiGrid-grid-xs-12.MuiGrid-grid-md-6.MuiGrid-grid-lg-4.css-obamm2 > div > div > div:nth-child(1) > div > div.MuiBox-root.css-1at62qq > p:nth-child(3)'
    css_url = '#__next > div.MuiBox-root.css-g9qx4c > main > div > div > div > div.MuiGrid-root.MuiGrid-item.MuiGrid-grid-xs-12.MuiGrid-grid-md-6.MuiGrid-grid-lg-4.css-obamm2 > div > div > div:nth-child(2) > div > div:nth-child(1) > div.MuiBox-root.css-19ambhl > a > h6'
    css_tel = '#__next > div.MuiBox-root.css-g9qx4c > main > div > div > div > div.MuiGrid-root.MuiGrid-item.MuiGrid-grid-xs-12.MuiGrid-grid-md-6.MuiGrid-grid-lg-4.css-obamm2 > div > div > div:nth-child(1) > div > div.MuiBox-root.css-1at62qq > p:nth-child(4)'


    ex.name = tools.get_information_from_css_link(css_name, throw_exception=True)
    ex.url = tools.get_information_from_css_link(css_url, timeout=0.5)
    ex.tel = tools.get_information_from_css_link(css_tel, timeout=0.5)
    ex.mail = get_mail()

    ex.street = tools.get_information_from_css_link(css_street, timeout=0.5)
    city  = tools.get_information_from_css_link(css_city, timeout=0.5).split(',')
    ex.city = city[0].strip()
    ex.postcode = city[1].strip()
    ex.country = tools.get_information_from_css_link(css_country, timeout=0.5)

    if tools.run_mode == RunMode.TESTING:
        print(str(ex))

def get_mail():
    i = 1
    while True:
        css_mail = f'#matchmaking_information > div > div:nth-child({i}) > div > div > p'
        try:
            mail = tools.get_information_from_css_link(css_mail, throw_exception=True, timeout=0.5)
            if "@" in mail:
                return mail
        except TimeoutException:
            return ""
        i += 1



if __name__ == "__main__":
    tools.open_link(exhibitor_list_link)
    tools.driver.maximize_window()
    accept_cookies()
    links = tools.get_links(get_exhibitor_links)
    tools.iterate_exhibitor_links(links, parse_exhibitor)