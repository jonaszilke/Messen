from selenium.common.exceptions import TimeoutException

from tools.ToolsMesse import Tools, RunMode
from tools.exhibitor import Exhibitor

tools = Tools(RunMode.RUN)

def parse_exhibitor(ex: Exhibitor, data):


    ex.name = data[0]
    ex.street = data[3]
    ex.city = data[4]
    ex.postcode = data[5]
    ex.country = data[6]
    ex.tel = data[7]
    ex.fax = data[8]
    ex.mail = data[9]
    ex.url = data[10]

if __name__ == "__main__":
    file_name = r'C:\Users\jonas\PycharmProjects\Messen\2024\05_May\data\gpec_exhibitorlist.txt'
    with open(file_name, 'r') as file:
        lines = file.readlines()

        for line in lines[1:]:
            split = line.split('\t')
            exhibitor: Exhibitor = Exhibitor()
            try:
                parse_exhibitor(exhibitor, split)
            except IndexError:
                pass
            finally:
                tools.save_exhibitor(exhibitor)
