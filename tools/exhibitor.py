import re

class Exhibitor:
    def __init__(self, name="", street="", postcode="", city="", country="", tel="", fax="", mail="", url="", info=""):
        self.name: str = name
        self.street: str = street
        self.postcode: str = postcode
        self.city: str = city
        self.country: str = country
        self.tel: str = tel
        self.fax: str = fax
        self.mail: str = mail
        self.url: str = url
        self.info: str = info

    def __str__(self):
        s = self.name + "\t" \
            + self.street + "\t" \
            + self.postcode + "\t" \
            + self.city + "\t" \
            + self.country + "\t" \
            + self.tel + "\t" \
            + self.fax + "\t" \
            + self.mail + "\t" \
            + self.url + "\t" \
            + self.info
        s = s.replace("\n", " ")
        return s + "\n"

    def split_save_code_city(self, city: str):
        city = city.strip()
        if city.startswith('DE ') or city.startswith('D-'):
            city = city.replace('DE ', '', 1).replace('D-', '', 1)
            self.country = 'Deutschland'
        city = city.strip()
        split_city = city.split(' ', 1)
        self.postcode = split_city[0]
        self.city = split_city[1]

    def add_tel_or_fax(self, info: str):
        if self.tel == '':
            self.tel = info
        else:
            self.fax = info

    def add_info(self, info: str):
        self.info = ';'.join([self.info, info.replace('\n', ';')]) if self.info != "" else info.replace('\n', ';')

    def sort_string(self, info: str):
        info = info.strip()
        if info == "" or info == self.name:
            return
        if self._is_phone(info):
            self.add_tel_or_fax(info)
        elif self._is_mail(info):
            self.mail = info
        elif self._is_url(info):
            self.url = info

        elif self._is_postcode_city(info):
            self.split_save_code_city(info)
        elif self.street == "":
            self.street = info
        elif self.city == "":
            if self._is_postcode_city(info):
                self.split_save_code_city(info)
            else:
                self.city = info
        elif self.country == "":
            self.country = info

    def sort_list(self, info: list[str]):
        for i in info:
            self.sort_string(i)

    def find_postcode_city(self, data: list[str]):
        for i,d in enumerate(data):
            if self._is_postcode_city(d):
                return i
        return -1

    def sort_address(self, address: list[str]):
        for idx, a in enumerate(address):
            address[idx] = a.strip()
        city_index = self.find_postcode_city(address)
        if city_index == -1:
            try:
                self.street = address[0]

                if self._is_postcode_city(address[1]):
                    self.split_save_code_city(address[1])
                    self.country = address[2]
                elif len(address) == 4:
                    self.postcode = address[1]
                    self.city = address[2]
                    self.country = address[3]
                else:
                    self.city = address[1]
                    self.country = address[2]
            except IndexError:
                pass
        else:
            self.split_save_code_city(address[city_index])
            try:
                self.street = address[city_index-1]
            except IndexError:
                pass
            try:
                self.country = address[city_index + 1]
            except IndexError:
                pass

    @staticmethod
    def _is_postcode_city(postcode: str):
        postcode_temp = postcode[2:] if postcode[0:2] == 'D-' else postcode
        split_address = postcode_temp.split(' ', 1)
        if len(split_address) < 2:
            return False
        return split_address[0].isdigit() and not split_address[1].isdigit()


    @staticmethod
    def _is_phone(info: str):
        info = info.replace(" ", "")
        phone_pattern = r'\+?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}'
        return re.fullmatch(phone_pattern, info)

    @staticmethod
    def _is_mail(info: str):
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        return re.fullmatch(email_pattern, info)

    @staticmethod
    def _is_url(info: str):
        url_pattern = r'(https?:\/\/)?(www\.)?[-a-zA-Z0-9:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()!@:%_\+.~#?&\/\/=]*)'
        return re.fullmatch(url_pattern, info)

