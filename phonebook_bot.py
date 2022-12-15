import telebot
import json
from phonebook_lib import\
    pb_view_all, \
    pb_view_search, \
    pb_add, \
    pb_delete, \
    pb_load, \
    pb_save
    
API_TOKEN = "5641081713:AAGgQT2BgXL2zTfVTZuIjoNIL0_JwjvDhtc"
bot = telebot.TeleBot(API_TOKEN)
add_flag = False
familia_flag = False
name_flag = False
otchestvo_flag = False
phone_flag = False
edit_flag = False
phone_clear_flag = False
cur_cont = {}

def send_contacts(chat_id, contacts_list):
    for cont in contacts_list:
        phones = ''
        for phone in cont['Телефон']:
            phones += phone + '\n'
        user_message = f"<b>№ контакта:</b> {cont['id']}\n<b>ФИО:\n</b>{cont['Фамилия']} {cont['Имя']}\n{cont['Отчество']}\n<b>Телефоны:</b>\n{phones}\n"
        bot.send_message(chat_id, user_message, parse_mode='HTML')

# Приветственное сообщение и список команд
@bot.message_handler(commands=['start'])
def start_message(message):
    # Описание работы
    bot.send_message(message.chat.id, "Добро пожаловать в телефонный бот-справочник." + \
        "\n/all - Вывести все контакты" + \
        "\n/search - Поиск контакта" + \
        "\n/add - Добавить контакт" + \
        "\n/delete - Удалить контакт" + \
        "\n/edit - Редактировать контакт" +\
        "\n/help - Справка по командам")

# Приветственное сообщение и список команд
@bot.message_handler(commands=['help'])
def start_message(message):
    # Описание работы
    bot.send_message(message.chat.id, "Добро пожаловать в телефонный бот-справочник." + \
        "\n/all - Вывести все контакты" + \
        "\n/search XXX - Поиск контакта по вхождению в него XXX" + \
        "\n/add - Добавить контакт" + \
        "\n/delete X - Удалить контакт с номером X (Укажите нужный номер контакта)" + \
        "\n/edit X - Редактировать контакт с номером X (Укажите нужный номер контакта)" +\
        "\n/help - Справка по командам")

# Вывод всех контактов
@bot.message_handler(commands=['all'])
def view_all_contacts(message):
    all_cont = pb_view_all()
    send_contacts(message.chat.id, all_cont)

# Поиск контакта
@bot.message_handler(commands=['search'])
def search_contacts(message):
    search_list = message.text.replace('/search', '').split(' ')
    for el in search_list:
        if el == '':
            search_list.remove('')
    found_cont = pb_view_search(search_list)
    send_contacts(message.chat.id, found_cont)

# Удаление контакта по его номеру
@bot.message_handler(commands=['del'])
def search_contacts(message):
    del_list = message.text.replace('/del', '').split(' ')
    for el in del_list:
        if el == '':
            del_list.remove('')
    pb_delete(del_list)
    bot.send_message(message.chat.id, 'Контакт удален')

# Добавление контакта
@bot.message_handler(commands=['add'])
def add_contacts(message):
    global add_flag
    global familia_flag
    global cur_cont
    add_flag = True
    familia_flag = True
    cur_cont['Фамилия'] = ''
    cur_cont['Имя'] = ''
    cur_cont['Отчество'] = ''
    cur_cont['Телефон'] = []
    bot.send_message(message.chat.id, 'Введите данные по новому контакту\nДля завершения ввода напишите "Готово"\nФамилия:')

# Редактирование контакта
@bot.message_handler(commands=['edit'])
def edit_contacts(message):
    global edit_flag, familia_flag, name_flag, otchestvo_flag, phone_flag, phone_clear_flag, cur_cont
    edit_list = message.text.replace('/edit', '').split(' ')
    for el in edit_list:
        if el == '':
            edit_list.remove('')
    cur_cont = pb_load(edit_list[0])
    edit_flag = True
    familia_flag = True
    phone_clear_flag = False
    bot.send_message(message.chat.id, 'Введите новую фамилию контакта\nВведите "Нет", если фамилию менять не требуется\nВведите "Готово", если больше ничего менять не нужно')
    
@bot.message_handler()
def calc_message(message):
    global add_flag, edit_flag, familia_flag, name_flag, otchestvo_flag, phone_flag, phone_clear_flag, cur_cont
    try:
        if add_flag == True:
            if message.text.lower() == "готово":
                familia_flag = False
                name_flag = False
                otchestvo_flag = False
                phone_flag = False
                add_flag = False
                pb_add(cur_cont)
                cur_cont = {}
                bot.send_message(message.chat.id, "Новый контакт добавлен.\nНапишите /all для просмотра всех контактов")
            elif familia_flag == True:
                cur_cont['Фамилия'] = message.text
                bot.send_message(message.chat.id, "Имя:")
                familia_flag = False
                name_flag = True
            elif name_flag == True:
                cur_cont['Имя'] = message.text
                bot.send_message(message.chat.id, "Отчество:")
                name_flag = False
                otchestvo_flag = True
            elif otchestvo_flag == True:
                cur_cont['Отчество'] = message.text
                bot.send_message(message.chat.id, "Телефон:")
                otchestvo_flag = False
                phone_flag = True
            elif phone_flag == True:
                cur_cont['Телефон'].append(message.text)
                bot.send_message(message.chat.id, "Еще Телефон (Или Готово):")
        if edit_flag == True:
            if message.text.lower() == "готово":
                familia_flag = False
                name_flag = False
                otchestvo_flag = False
                phone_flag = False
                edit_flag = False
                pb_save(cur_cont)
                cur_cont = {}
                bot.send_message(message.chat.id, "Изменения по контакту сохранены.\nНапишите /all для просмотра всех контактов")
            elif familia_flag == True:
                if message.text.lower() != "нет":
                    cur_cont['Фамилия'] = message.text
                familia_flag = False
                name_flag = True
                bot.send_message(message.chat.id, 'Введите новое имя контакта\nВведите "Нет", если имя менять не требуется\nВведите "Готово", если больше ничего менять не нужно')
            elif name_flag == True:
                if message.text.lower() != "нет":
                    cur_cont['Имя'] = message.text
                name_flag = False
                otchestvo_flag = True
                bot.send_message(message.chat.id, 'Введите новое отчество контакта\nВведите "Нет", если отчество менять не требуется\nВведите "Готово", если больше ничего менять не нужно')
            elif otchestvo_flag == True:
                if message.text.lower() != "нет":
                    cur_cont['Отчество'] = message.text
                otchestvo_flag = False
                phone_flag = True
                bot.send_message(message.chat.id, 'Введите измененные телефоны контакта\nВведите "Нет", если телефоны менять не требуется\nВведите "Готово", если больше ничего менять не нужно')
            elif phone_flag == True:
                if message.text.lower() != "нет":
                    if phone_clear_flag == False:
                        cur_cont['Телефон'] = []
                        phone_clear_flag = True
                    cur_cont['Телефон'].append(message.text)
                bot.send_message(message.chat.id, 'Еще Телефон (Или "Готово"):')
    except:
        bot.send_message(message.chat.id, "Команда не распознана.\nНажмите /help для вывода списка доступных команд.")

print("Бот работает")
bot.polling()