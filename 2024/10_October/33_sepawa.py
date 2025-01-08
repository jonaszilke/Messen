import time

from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor

exhibitor_list_link = "https://sepawa.com/congress/besucher/ausstellerliste/"
tools = Tools(RunMode.RUN)


def accept_cookies():
    css_accept = 'a._brlbs-btn._brlbs-btn-accept-all._brlbs-cursor'
    tools.click_css_link(css_accept)


def get_exhibitor_links():
    while True:
        try:
            css_load_more = '#post-1855 > div > div > div > div.et_pb_section.et_pb_section_11.et_section_regular > div.et_pb_row.et_pb_row_7.et_pb_gutters2 > div > div.et_pb_module.et_pb_de_mach_archive_loop.et_pb_de_mach_archive_loop_0.grid-layout-grid.clearfix.main-loop.loadmore-align-.main-archive-loop.same-height-cards.loadmore-enabled.load_more_on > div > div.dmach-loadmore.et_pb_button'
            tools.scroll_css_into_view(css_load_more)
            tools.driver.execute_script("window.scrollBy(0, -200);")
            button_text = tools.get_information_from_css_link(css_load_more)
            if button_text == 'Mehr laden':
                tools.click_css_link(css_load_more)
            else:
                time.sleep(2)
        except Exception as NoSuchElementException:
            break
    links = []
    filter_str = 'https://sepawa.com/congress/aussteller/'
    prefix = ''
    links += [prefix + l for l in tools.find_links(filter_str=filter_str)]

    return links


def parse_exhibitor(ex: Exhibitor):
    css_name = '#main-content > div > div > div.et_pb_section.et_pb_section_1_tb_body.et_section_regular > div.et_pb_row.et_pb_row_0_tb_body.et_pb_row_3-4_1-4 > div.et_pb_column.et_pb_column_3_4.et_pb_column_0_tb_body.et_pb_css_mix_blend_mode_passthrough > div > div > div > div.dmach-acf-item-content > h1'
    css_address = '#main-content > div > div > div.et_pb_section.et_pb_section_1_tb_body.et_section_regular > div.et_pb_row.et_pb_row_1_tb_body > div > div.et_pb_module.et_pb_de_mach_acf_item.et_pb_de_mach_acf_item_3_tb_body.dmach-text-before-pos-same_line.dmach-label-pos-same_line.dmach-vertical-alignment-middle.et_pb_de_mach_alignment_.dmach-acf-has-value.dmach-image-icon-placement-left > div > div > div.dmach-acf-item-content > p'
    css_mail = '#main-content > div > div > div.et_pb_section.et_pb_section_1_tb_body.et_section_regular > div.et_pb_row.et_pb_row_1_tb_body > div > div.et_pb_module.et_pb_de_mach_acf_item.et_pb_de_mach_acf_item_4_tb_body.dmach-text-before-pos-same_line.dmach-label-pos-same_line.dmach-vertical-alignment-middle.et_pb_de_mach_alignment_.dmach-acf-has-value.dmach-image-icon-placement-left > div > div > div.dmach-acf-item-content > a'

    timeout = 0.1
    ex.name = tools.get_information_from_css_link(css_name)
    ex.mail = tools.get_information_from_css_link(css_mail, timeout=timeout)

    address = tools.get_information_from_css_link(css_address, timeout=timeout).replace('Adresse\n', '')
    address = address.split('|')
    if len(address) == 1:
        address = address.split(',')
    ex.sort_address(address)
    ex.add_info(address)


if __name__ == "__main__":
    tools.open_link(exhibitor_list_link)
    accept_cookies()
    links = tools.get_links(get_exhibitor_links)
    tools.iterate_exhibitor_links(links, parse_exhibitor)
