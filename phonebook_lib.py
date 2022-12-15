import json

# Возвращает словарь со списком всех контактов
def pb_view_all():
    with open('phonebook.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

# Возвращает словарь со списком всех контактов, удовлетворяющим условиям поиска
def pb_view_search(search_list):
    with open('phonebook.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    found_data = []
    for line in data:
        search_flag = 1
        for el in search_list:
            temp_search = 0
            if el.lower() in line["Фамилия"].lower(): temp_search = 1
            if el.lower() in line["Имя"].lower(): temp_search = 1
            if el.lower() in line["Отчество"].lower(): temp_search = 1
            for phone in line["Телефон"]:
                if el.lower() in phone.lower(): temp_search = 1
            search_flag = search_flag * temp_search
        if search_flag == 1: found_data.append(line)
    return found_data

# Добавляет в телефонную книгу новый контакт
def pb_add(cur_cont):
    with open('phonebook.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    max_num = 0
    for line in data:
        if line['id'] > max_num:
            max_num = line['id']
    cont_dict = {}
    cont_dict['id'] = max_num + 1
    cont_dict['Фамилия'] = cur_cont['Фамилия']
    cont_dict['Имя'] = cur_cont['Имя']
    cont_dict['Отчество'] = cur_cont['Отчество']
    cont_dict['Телефон'] = cur_cont['Телефон']
    data.append(cont_dict)
    with open('phonebook.json', 'w', encoding='utf-8') as write_file:
        json.dump(data, write_file)

# Удаляет из телефонной книги указанный контакт
def pb_delete(cont_num):
    with open('phonebook.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    del_index = []
    for i in range(len(data)):
        if str(data[i]['id']) in cont_num:
            del_index.append(i)
    for i in del_index:
        data.pop(i)
    with open('phonebook.json', 'w', encoding='utf-8') as write_file:
        json.dump(data, write_file)

# Загрузка данных по указанному контакту    
def pb_load(cont_num):
    with open('phonebook.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    for line in data:
        if str(line['id']) == cont_num:
            return line
        
# Сохранение данных по указанному контакту
def pb_save(cur_cont):
    with open('phonebook.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    for i in range(len(data)):
        if str(data[i]['id']) == str(cur_cont["id"]):
            data[i] = cur_cont
    with open('phonebook.json', 'w', encoding='utf-8') as write_file:
        json.dump(data, write_file)