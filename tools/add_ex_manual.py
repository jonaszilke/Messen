from tools.exhibitor import Exhibitor

exhibition_name = input('Exhibition Name:')

finished = False

while not finished:
    ex = Exhibitor()
    ex.name = input('Name: ')
    ex.street = input('Street: ')
    ex.postcode = input('Postcode: ')
    ex.city = input('City: ')
    ex.country = input('Country: ')
    ex.tel = input('Tel: ')
    ex.fax = input('Fax: ')
    ex.mail = input('Mail: ')
    ex.url = input('Url: ')

    with open(exhibition_name + '.txt', 'w', encoding='utf-8') as file:
        file.write(str(ex))


    finished = True if input("Finished? (Type 'yes')").lower() == 'yes' else False
