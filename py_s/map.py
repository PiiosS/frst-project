import sdata
import pymysql
import requests
import re


def del_sign(text):
    return re.sub(r'[!@#$%^&*\";:?]', '', text)
def conn():
    return pymysql.connect(host=sdata.HOST, user=sdata.USER, password=sdata.PASSWORD, database=sdata.DATABASE)
def schedule():
    url = "https://api.xn--80aai1dk.xn--p1ai/api/schedule?range=1"  #&subdivision_cod=1&group_name=5134"

    PAIR_TIMES = {
        '1': '08:30-10:00',
        '2': '10:15-11:45',
        '3': '12:20-13:50',
        '4': '14:00-15:30',
        '5': '15:45-17:15',
        '6': '17:30-19:00',
        '7': '19:10-20:40',
    }

    connection = conn()
    cursor = connection.cursor()
    cursor.execute("""TRUNCATE TABLE schedule""")


    response = requests.get(url)
    data = response.json()
    print(f': {response.status_code} ({len(data)})')
    for schedule in data:
        DATEarr = schedule['date'].split('.')
        DATE = str(DATEarr[2] + '-' + DATEarr[1] + '-' + DATEarr[0])
        pair=PAIR_TIMES[schedule['pair'].strip()]
        subject = del_sign(schedule['subject'].strip())
        if subject=='':
            subject = del_sign(schedule['prim'].strip())
        signature = del_sign(schedule['signature'].strip())
        classroom = del_sign(schedule['classroom'].strip())
        classroom_building = del_sign(schedule['classroom_building'].strip())
        group_name = del_sign(schedule['group_name'].strip())

        insert_query = f"""
                INSERT INTO `schedule`(`sdate`, `pair`, `subject`, `signature`, `classroom`, `classroom_building`, `group_name`) VALUES ("{DATE}","{pair}","{subject}","{signature}","{classroom}","{classroom_building}","{group_name}")
                """
        connection = conn()
        cursor = connection.cursor()
        cursor.execute(insert_query)
# Подтверждение изменений в базе данных и закрытие соединения utf8_unicode_ci

        connection.commit()
    connection.close()
x=1+1
#schedule()
