import telebot
import pymysql
from datetime import date, timedelta
import data

bot = telebot.TeleBot(data.TOKEN)
db_connection = pymysql.connect(host=data.HOST, user=data.USER, password=data.PASSWORD, database=data.DATABASE)
db_cursor = db_connection.cursor()
message=''

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет, чем я могу тебе помочь?")
    bot.send_message(message.chat.id, "Для вывода данных на текущий день напиши /today, для вывода данных на следующий день напиши /next_day")

@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, "Для вывода данных на текущий день напиши /today, для вывода данных на следующий день напиши /next_day")

@bot.message_handler(commands=['today'])
def get_today_data(message):
    current_date = date.today()
    print(message.chat.id,"Запросил",current_date)
    try:
        db_cursor.execute("SELECT date, pair, signature, classroom, classroom_building, subject FROM schedule WHERE date = %s", (current_date,))
        rows = db_cursor.fetchall()
        if rows:
            message_text = "Данные на текущий день:\n"
            for row in rows:
                date_str, pair, signature, classroom, classroom_building, subject = row
                message_text += f"Дата: {date_str}, Время занятия: {pair}, Преподаватель: {signature}, Предмет: {subject}, Кабинет: {classroom}, Учебный корпус: {classroom_building}\n"
        else:
            message_text = "На текущий день данных нет"
    except:
        message_text = "Произошла ошибка при получении данных из базы данных"
    bot.send_message(message.chat.id, message_text)

@bot.message_handler(commands=['next_day'])
def get_next_day_data(message):
    next_date = date.today() + timedelta(days=1)
    print(message.chat.id,"Запросил",next_date)
    try:
        db_cursor.execute("SELECT date, pair, signature, classroom, classroom_building, subject FROM schedule WHERE date = %s", (next_date,))
        rows = db_cursor.fetchall()
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
@bot.message_handler(commands=['Ксюша'])
def ksenia_msg(message):
    print('Отправляю 962847585')
    message_text = "Ксюша, тебе приходят сообщения от бота?"
    img = open('cat.jpg', 'rb')
    bot.send_photo(5169161016, img)
    bot.send_message(message.chat.id, message_text)

@bot.message_handler(commands=['стоп'])
def stop_msg(message):
    print('Протокол "пока"')
    message_text = "Ня, пока ❤️"
    bot.send_message(message.chat.id, message_text)
    bot.stop_bot()
bot.polling()