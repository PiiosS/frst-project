import telebot
import pymysql
from datetime import date, timedelta
import data
import map
import csv


bot = telebot.TeleBot(data.TOKEN)
connection = pymysql.connect(host=data.HOST, user=data.USER, password=data.PASSWORD, database=data.DATABASE)
cursor = connection.cursor()
message = ''
message_text = ''


def log(user_id, first_name, user_name, user_message, bot_response):
    insert_query = f"""INSERT INTO log (time_m, user_id, first_name, user_name, user_message, bot_response)
     VALUES (NOW(),'{user_id}','{first_name}','{user_name}','{user_message}','{bot_response}')"""
    try:
        cursor.execute(insert_query)
        connection.commit()
    except: bot_response="Ошибка подключения к БД для логирования "+bot_response
    file_path = 'id.csv'
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([user_id, first_name, user_name, user_message, bot_response])
        print(user_id, first_name, user_name, user_message, bot_response)


@bot.message_handler(commands=['update'])
def start_message(message):
    try:
        map.schedule()
        message_text='Обновлено'
    except:
        message_text='Ошибка обновления'
    bot.send_message(message.chat.id, message_text)
    log(message.chat.id, message.from_user.first_name, message.from_user.username, message.text, message_text)


@bot.message_handler(commands=['start'])
def start_message(message):
    message_text='Для вывода данных на текущий день напиши /today, для вывода данных на следующий день напиши /next_day'
    bot.send_message(message.chat.id, message_text)
    log(message.chat.id, message.from_user.first_name, message.from_user.username, message.text, message_text)

@bot.message_handler(commands=['help'])
def help_message(message):
    message_text="Для вывода данных на текущий день напиши /today, для вывода данных на следующий день напиши /next_day"
    bot.send_message(message.chat.id,message_text)
    log(message.chat.id, message.from_user.first_name, message.from_user.username, message.text, message_text)


@bot.message_handler(commands=['today'])
def get_today_data(message):
    current_date = date.today()
    print(message.chat.id, "Запросил", current_date)
    try:
        cursor.execute(
            "SELECT date, pair, signature, classroom, classroom_building, subject FROM schedule WHERE date = %s LIMIT 5",
            current_date)
        rows = cursor.fetchall()
        if rows:
            message_text = "Данные на текущий день:\n"
            for row in rows:
                date_s, pair, signature, classroom, classroom_building, subject = row
                message_text += f"Дата: {date_s}, Время занятия: {pair}, Преподаватель: {signature}, Предмет: {subject}, Кабинет: {classroom}, Учебный корпус: {classroom_building}\n"
        else:
            message_text = "На текущий день данных нет"
    except:
        message_text = "На текущий день данных нет"
    bot.send_message(message.chat.id, message_text)
    log(message.chat.id, message.from_user.first_name, message.from_user.username, message.text, message_text)


@bot.message_handler(commands=['next_day'])
def get_next_day_data(message):
    next_date = date.today() + timedelta(days=1)
    print(message.chat.id, "Запросил", next_date)
    try:
        cursor.execute(
            "SELECT date, pair, signature, classroom, classroom_building, subject FROM schedule WHERE date = %s LIMIT 5",
            (next_date,))
        rows = cursor.fetchall()
        if rows:
            message_text = "Данные на следующий день:\n"
            for row in rows:
                date_str, pair, signature, classroom, classroom_building, subject = row
                message_text += f"Дата: {date_str}, Время занятия: {pair}, Преподаватель: {signature}, Предмет: {subject}, Кабинет: {classroom}, Учебный корпус: {classroom_building}\n"
        else:
            message_text = "На следующий день данных нет"
    except:
        message_text = "На следующий день данных нет"
    bot.send_message(message.chat.id, message_text)
    log(message.chat.id, message.from_user.first_name, message.from_user.username, message.text, message_text)


@bot.message_handler(commands=['Ксюша'])
def ksenia_msg(message):
    print('Отправляю 962847585')
    message_text = "Ксюша, тебе приходят сообщения от бота?"
    img = open('cat.jpg', 'rb')
    bot.send_photo(5169161016, img)
    bot.send_message(message.chat.id, message_text)
    log(message.chat.id, message.from_user.first_name, message.from_user.username, message.text, message_text)


@bot.message_handler(commands=['стоп'])
def stop_msg(message):
    print('Протокол "пока"')
    message_text = "Ня, пока"
    bot.send_message(message.chat.id, message_text)
    log(message.chat.id, message.from_user.first_name, message.from_user.username, message.text, message_text)
    bot.stop_bot()

@bot.message_handler()
def all_message(message):
    log(message.chat.id, message.from_user.first_name, message.from_user.username, message.text, message_text)

bot.polling()

