from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor

exhibitor_list_link = "https://www.fmb-messe.de/de/exhibitor/?_per_page=96"
tools = Tools(RunMode.RUN)


def accept_cookies():
    css_accept = '#iubenda-cs-banner > div > div > div > div.iubenda-cs-opt-group > div.iubenda-cs-opt-group-consent > button.iubenda-cs-accept-btn.iubenda-cs-btn-primary'
    try:
        tools.click_css_link(css_accept)
    except:
        input('Accept Cookies manually!!!')


def get_exhibitor_links():

    links = []
    filter_str = 'https://www.fmb-messe.de/de/exhibitor/'
    prefix = ''

    for page in range(1, 6):
        link = f'https://www.fmb-messe.de/de/exhibitor/?_paged={page}&_per_page=96'
        tools.open_link(link)
        links += [prefix + l for l in tools.find_links(filter_str=filter_str)]
    return links


def parse_exhibitor(ex: Exhibitor):
    css_name = '#content > div > div > section.elementor-section.elementor-top-section.elementor-element.elementor-element-e09669d.elementor-section-content-top.elementor-section-boxed.elementor-section-height-default.elementor-section-height-default > div > div.elementor-column.elementor-col-50.elementor-top-column.elementor-element.elementor-element-531d462c > div > div.elementor-element.elementor-element-b1452fc.elementor-widget.elementor-widget-heading > div > h1'
    css_postcode = '#content > div > div > section.elementor-section.elementor-top-section.elementor-element.elementor-element-4d3b8125.elementor-section-content-top.elementor-section-stretched.elementor-section-boxed.elementor-section-height-default.elementor-section-height-default > div > div.elementor-column.elementor-col-50.elementor-top-column.elementor-element.elementor-element-31e8ba18 > div > div.elementor-element.elementor-element-6aa30c07.elementor-align-left.elementor-widget.elementor-widget-post-info > div > ul > li.elementor-icon-list-item.elementor-repeater-item-bd10f2c.elementor-inline-item > span.elementor-icon-list-text.elementor-post-info__item.elementor-post-info__item--type-custom'
    css_city = '#content > div > div > section.elementor-section.elementor-top-section.elementor-element.elementor-element-4d3b8125.elementor-section-content-top.elementor-section-stretched.elementor-section-boxed.elementor-section-height-default.elementor-section-height-default > div > div.elementor-column.elementor-col-50.elementor-top-column.elementor-element.elementor-element-31e8ba18 > div > div.elementor-element.elementor-element-6aa30c07.elementor-align-left.elementor-widget.elementor-widget-post-info > div > ul > li.elementor-icon-list-item.elementor-repeater-item-a6a4d86.elementor-inline-item > span'
    css_country = '#content > div > div > section.elementor-section.elementor-top-section.elementor-element.elementor-element-4d3b8125.elementor-section-content-top.elementor-section-stretched.elementor-section-boxed.elementor-section-height-default.elementor-section-height-default > div > div.elementor-column.elementor-col-50.elementor-top-column.elementor-element.elementor-element-31e8ba18 > div > div.elementor-element.elementor-element-6aa30c07.elementor-align-left.elementor-widget.elementor-widget-post-info > div > ul > li.elementor-icon-list-item.elementor-repeater-item-8694a23.elementor-inline-item > span > span > span'
    css_url = '#content > div > div > section.elementor-section.elementor-top-section.elementor-element.elementor-element-4d3b8125.elementor-section-content-top.elementor-section-stretched.elementor-section-boxed.elementor-section-height-default.elementor-section-height-default > div > div.elementor-column.elementor-col-50.elementor-top-column.elementor-element.elementor-element-31e8ba18 > div > div.elementor-element.elementor-element-6e36ae44.elementor-align-left.elementor-widget.elementor-widget-post-info > div > ul > li > a > span.elementor-icon-list-text.elementor-post-info__item.elementor-post-info__item--type-custom'

    timeout = 0.1
    ex.name = tools.get_information_from_css_link(css_name)
    ex.url = tools.get_information_from_css_link(css_url, timeout=timeout)

    ex.postcode = tools.get_information_from_css_link(css_postcode, timeout=timeout)[:-1]
    ex.city = tools.get_information_from_css_link(css_city, timeout=timeout)[:-1]
    ex.country = tools.get_information_from_css_link(css_country, timeout=timeout)

    i = 0


if __name__ == "__main__":
    tools.open_link(exhibitor_list_link)
    accept_cookies()
    links = tools.get_links(get_exhibitor_links)
    tools.iterate_exhibitor_links(links, parse_exhibitor)
