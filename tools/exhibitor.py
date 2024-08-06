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

        self.postcode = city[:5]
        self.city = city[6:]

    def add_tel_or_fax(self, info: str):
        if self.tel == '':
            self.tel = info
        else:
            self.fax = info

    def add_info(self, info: str):
        self.info = ';'.join([self.info, info.replace('\n', ';')]) if self.info != "" else info.replace('\n', ';')

    def sort_string(self, info: str):
        info = info.strip()
        if self._is_phone(info):
            self.add_tel_or_fax(info)
        elif self._is_mail(info):
            self.mail = info
        elif self._is_url(info):
            self.url = info


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
        url_pattern = r'[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)'
        return re.fullmatch(url_pattern, info)

    @staticmethod
    def _is_url(info: str):
        url_pattern = r'[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)'
        return re.fullmatch(url_pattern, info)

