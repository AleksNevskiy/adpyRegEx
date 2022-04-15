
# читаем адресную книгу в формате CSV в список contacts_list
import csv
import re

def reading():
    with open("phonebook_raw.csv") as f:
      rows = csv.reader(f, delimiter=",")
      contacts_list = list(rows)
    return contacts_list
# TODO 1: выполните пункты 1-3 ДЗ
# Передосим записи из дублей
def transfer_of_duplicates(contacts_list, pattern_full_name):
    temp_list = []
    for l in contacts_list:
        temp_list.append(re.findall(pattern_full_name, l[0])+(re.findall(pattern_full_name, l[1]))+re.findall(pattern_full_name, l[2]))
    for x in range(0,len(contacts_list)):
      for y in range(0, len(contacts_list)):
        if len(temp_list[x]) != False and len(temp_list[y]) != False:
          if temp_list[x][0] == temp_list[y][0] and temp_list[x][1] == temp_list[y][1]:
            for a in range(0,len(contacts_list[0])):
              if not contacts_list[x][a]:
                contacts_list[x][a] = contacts_list[y][a]
    return contacts_list
# Вносим обработаные днные в новый список
def data_processing(contacts_list, pattern_full_name):
    super_contact_list = []
    pattern_phone = r'(\+7|8)?\s*\(?(\d{3})\)?\W?(\d{3})\-?(\d{2})\-?(\d+)\s*\(?([а-яА-я]+[.])?\s*(\d+)?\)?'
    pattern_sub_phone = r'+7(\2)\3-\4-\5 \6\7'
    for l in range(0,len(contacts_list)):
        inner_contact_list = (re.findall(pattern_full_name, contacts_list[l][0])+(re.findall(pattern_full_name, contacts_list[l][1]))+re.findall(pattern_full_name, contacts_list[l][2]))
        if len(inner_contact_list) == 2:
            inner_contact_list.append(None)
        elif len(inner_contact_list) > 3:
            del inner_contact_list[3:(len(inner_contact_list))]
        if len(inner_contact_list) != False:
            if len(contacts_list[l][-4]) != False:
                inner_contact_list.insert(3, (contacts_list[l][-4]))
            else:
                inner_contact_list.insert(3, (None))
            if len(contacts_list[l][-3]) != False:
                inner_contact_list.insert(4, (contacts_list[l][-3]))
            else:
                inner_contact_list.insert(4, (None))
            if len(contacts_list[l][-2]) != False:
                sub_phone = re.sub(pattern_phone, pattern_sub_phone, contacts_list[l][-2])
                inner_contact_list.insert(5, sub_phone.strip())
            else:
                inner_contact_list.insert(5, (None))
            if len(contacts_list[l][-1]) != False:
                inner_contact_list.insert(6, (contacts_list[l][-1]))
            else:
                inner_contact_list.insert(6, (None))

        super_contact_list.append(inner_contact_list)
    super_contact_list[0] = ['lastname','firstname','surname','organization','position','phone','email']
    return super_contact_list
# Удаляем дубли
def clearing_of_duplicates(super_contact_list):
    for x_1 in range(0, len(super_contact_list)):
        for y_1 in range(0, len(super_contact_list)):
            if y_1 in range(0, len(super_contact_list)) and x_1 in range(0, len(super_contact_list)):
                if super_contact_list[x_1][0] == super_contact_list[y_1][0] and super_contact_list[x_1][1] == super_contact_list[y_1][1] and x_1 != y_1:
                    super_contact_list.pop(y_1)
    return super_contact_list

# TODO 2: сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
def writing(super_contact_list):
    with open("phonebook.csv", "w", newline='') as f:
      datawriter = csv.writer(f, delimiter=',')
      datawriter.writerows(super_contact_list)


if __name__ == '__main__':
    pattern_full_name = r'([А-Я][а-я]+)'
    writing(clearing_of_duplicates(data_processing(transfer_of_duplicates(reading(), pattern_full_name), pattern_full_name)))
