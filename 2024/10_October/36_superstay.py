from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor

exhibitor_list_link = "https://superstay.live/ausstellerliste/"
tools = Tools(RunMode.RUN)


def accept_cookies():
    css_accept = '#BorlabsCookieBox > div > div > div > div.cookie-box > div > div.row._brlbs-button-area > div:nth-child(1) > p'
    tools.click_css_link(css_accept)



if __name__ == "__main__":
    tools.open_link(exhibitor_list_link)
    accept_cookies()

    css_name = 'h4.elementor-heading-title.elementor-size-default'
    name_elements = tools.get_elements_by_css(css_name)
    names = [e.text for e in name_elements]

    css_url = 'a.elementor-button.elementor-button-link.elementor-size-sm'
    url_elements = tools.get_elements_by_css(css_url)
    urls = [e.get_attribute("href") for e in url_elements[-len(names):]]

    zipped = zip(names, urls)
    for name, url in zipped:
        ex = Exhibitor(name=name, url=url)
        tools.save_exhibitor(ex)

