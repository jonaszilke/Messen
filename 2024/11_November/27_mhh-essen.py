from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor

exhibitor_list_link = "https://www.mhh-essen.de/nrws-groesste-verbrauchermesse/ausstellerliste/"
tools = Tools(RunMode.RUN)

def accept_cookies():
    tools.click_css_link( '#uc-btn-accept-banner')


def get_exhibitor_links():
    tools.scroll()
    filter_str = '/nrws-groesste-verbrauchermesse/ausstellerliste/detail/'
    prefix = 'https://www.mhh-essen.de'
    links = [prefix + s.replace('\n', '').replace('\t', '') for s in tools.find_links(filter_str=filter_str)]
    return links


def parse_exhibitor(exhibitor: Exhibitor):
    css_name = '#zeile_aussteller_head > div > div > div.inner.element.overlay-dark.no-mm-login > div > div:nth-child(1) > h2'
    css_name2 = '#zeile_aussteller_head > div > div > div > div > div:nth-child(1) > h2'
    css_adresse = '#zeile_aussteller_infoblock > div > div.col.first > div > div.col.first > div > address'

    css_url = '#zeile_aussteller_infoblock > div > div.col.first > div > div.col.first > div > ul > li:nth-child(1) > a'
    css_info = '#zeile_aussteller_infoblock > div > div.col.first > div > div.col.last > div'


    exhibitor.name = tools.get_information_from_css_link(css_name)
    if exhibitor.name == '':
        exhibitor.name = tools.get_information_from_css_link(css_name2)
    exhibitor.url = tools.get_href_from_css_link(css_url)

    address = tools.get_information_from_css_link(css_adresse)
    address_split = address.split('\n')
    exhibitor.street = address_split[0]
    exhibitor.split_save_code_city(address_split[1])


    full_info = tools.get_information_from_css_link(css_info)
    split_info(exhibitor, full_info)
    pass

def split_info(exhibitor: Exhibitor, data: str):
    data = data.split("\n")
    for i, d in enumerate(data):
        if '+' in d or "".join(d.split()).isdigit():
            exhibitor.add_tel_or_fax(d)
        elif 'E-Mail' in data[i]:
            css_mail = f'#zeile_aussteller_infoblock > div > div.col.first > div > div.col.last > div > ul > li:nth-child({i-1}) > a'
            mail = tools.get_href_from_css_link(css_mail).replace('mailto:', '')
            exhibitor.mail = mail
        else:
            exhibitor.add_info(d)




if __name__ == "__main__":
    tools.open_link(exhibitor_list_link)
    accept_cookies()
    links = tools.get_links(get_exhibitor_links)
    tools.iterate_exhibitor_links(links, parse_exhibitor)
