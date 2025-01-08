import time

from selenium.common.exceptions import TimeoutException

from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor

exhibitor_list_link = "https://connect.buchmesse.de/newfront/marketplace/exhibitors?pageNumber=1&limit=12"
tools = Tools(RunMode.RUN)


def accept_cookies():
    input('Accept Cookies')


def get_exhibitor_links():
    filter_str = '/newfront/exhibitor/'
    prefix = 'https://connect.buchmesse.de'
    links = []
    for i in range(1,366):
        link = f"https://connect.buchmesse.de/newfront/marketplace/exhibitors?pageNumber={i}&limit=12"
        tools.open_link(link)
        time.sleep(2)
        tools.scroll()

        links += [prefix + l for l in tools.find_links(filter_str=filter_str)]
    return links


def parse_exhibitor(ex: Exhibitor):
    css_name = '#__next > div.MuiBox-root.css-g9qx4c > div.MuiBox-root.css-1roqr68 > main > div > div > div > div > div.MuiGrid-root.MuiGrid-item.MuiGrid-grid-xs-12.MuiGrid-grid-md-6.MuiGrid-grid-lg-4.css-obamm2 > div > div > div:nth-child(1) > div > div.MuiBox-root.css-qexdkq > h2'
    css_name = 'h2[data-styleid="profile-card-user-name"]'
    css_street = '#__next > div.MuiBox-root.css-g9qx4c > div.MuiBox-root.css-1roqr68 > main > div > div > div > div > div.MuiGrid-root.MuiGrid-item.MuiGrid-grid-xs-12.MuiGrid-grid-md-6.MuiGrid-grid-lg-4.css-obamm2 > div > div > div:nth-child(1) > div > div.MuiBox-root.css-1at62qq > p:nth-child(1)'
    css_street = '#__next > div.MuiBox-root.css-g9qx4c > main > div > div > div > div.MuiGrid-root.MuiGrid-item.MuiGrid-grid-xs-12.MuiGrid-grid-md-6.MuiGrid-grid-lg-4.css-obamm2 > div > div > div:nth-child(1) > div > div.MuiBox-root.css-1at62qq > p:nth-child(1)'
    css_city = '#__next > div.MuiBox-root.css-g9qx4c > main > div > div > div > div.MuiGrid-root.MuiGrid-item.MuiGrid-grid-xs-12.MuiGrid-grid-md-6.MuiGrid-grid-lg-4.css-obamm2 > div > div > div:nth-child(1) > div > div.MuiBox-root.css-1at62qq > p:nth-child(2)'
    css_country = '#__next > div.MuiBox-root.css-g9qx4c > main > div > div > div > div.MuiGrid-root.MuiGrid-item.MuiGrid-grid-xs-12.MuiGrid-grid-md-6.MuiGrid-grid-lg-4.css-obamm2 > div > div > div:nth-child(1) > div > div.MuiBox-root.css-1at62qq > p:nth-child(3)'
    css_url = '#__next > div.MuiBox-root.css-g9qx4c > main > div > div > div > div.MuiGrid-root.MuiGrid-item.MuiGrid-grid-xs-12.MuiGrid-grid-md-6.MuiGrid-grid-lg-4.css-obamm2 > div > div > div:nth-child(3) > div > div > div.MuiBox-root.css-19ambhl > a > h6'

    ex.name = tools.get_information_from_css_link(css_name, throw_exception=True)
    ex.url = tools.get_information_from_css_link(css_url, throw_exception=False, timeout=0.5)

    ex.street = tools.get_information_from_css_link(css_street, throw_exception=False, timeout=0.5)
    city  = tools.get_information_from_css_link(css_city, throw_exception=False, timeout=0.5).split(',')
    ex.country = tools.get_information_from_css_link(css_country, throw_exception=False, timeout=0.5)
    ex.city = city[0].strip()
    ex.postcode = city[1].strip()

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
        except:
            return ""
        i += 1


if __name__ == "__main__":
    tools.open_link(exhibitor_list_link)
    accept_cookies()
    links = tools.get_links(get_exhibitor_links)
    tools.iterate_exhibitor_links(links, parse_exhibitor)
