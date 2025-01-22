from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor


exhibitor_list_link = "https://osc.messe-dortmund.de/whdo/servlet/rubin.osc.bis.BisServlet?ishop_id2=&spr=D&FWD_spr=D&k2=HAVZ&aktMenueId=BIS_SEARCH&act=showform&k=AVZ&ishop_id=HE24_AVZ&vs=null&t=0701144252"
tools = Tools(RunMode.RUN)


def accept_cookies():
    css_accept = 'button.cookie_banner_button'
    tools.click_css_link(css_accept)


def get_exhibitor_links():
    links = []
    filter_str = r'rubin.osc.bis.BisServlet\?act=showdata&ipaeposExtid='
    prefix = 'https://osc.messe-dortmund.de/whdo/servlet/'

    css_first_letter = f'#searchForm > div:nth-child(17) > div.az-liste > a:nth-child(1)'
    tools.click_css_link(css_first_letter)

    css_links = [f'#searchForm > div:nth-child(16) > div.az-liste > a:nth-child({i})' for i in range(26,0,-1)]
    css_links.append('#searchForm > div:nth-child(16) > div.az-weitere > a')
    for css_letter in css_links:
        tools.click_css_link(css_letter)
        links += [prefix + l for l in tools.find_links(filter_str=filter_str)]

    return links


def parse_exhibitor(ex: Exhibitor):
    css_data = '.inhalt-links'

    data = tools.get_information_from_css_link(css_data)
    data = data.replace('Tel.:', '').replace('Email:', '').replace('E-Mail:','').replace('Fax:', '').splitlines()

    remove_list = ['Standnummer:']
    for s in remove_list:
        for d in data[1:]:
            if s in d or d == '':
                data.remove(d)

    ex.name = data[0]
    ex.sort_list(data)

    if tools.run_mode == RunMode.TESTING:
        print(str(ex))


if __name__ == "__main__":
    tools.open_link(exhibitor_list_link)
    accept_cookies()
    links = tools.get_links(get_exhibitor_links)
    tools.iterate_exhibitor_links(links, parse_exhibitor)