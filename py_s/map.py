import data.py
import pymysql
import requests

connection = pymysql.connect(host=data.HOST, user=data.USER, password=data.PASSWORD, database=data.DATABASE)
cursor = connection.cursor()



url = "https://api.xn--80aai1dk.xn--p1ai/api/schedule?range=1&subdivision_cod=1&group_name=5134"

PAIR_TIMES = {
    '1': '08:30-10:00',
    '2': '10:15-11:45',
    '3': '12:20-13:50',
    '4': '14:00-15:30',
    '5': '15:45-17:15',
    '6': '17:30-19:00',
    '7': '19:10-20:40',
}
cursor.execute("""TRUNCATE TABLE schedule""")
with open('schedule_data.csv', mode='w', newline='') as csvfile:
    #fieldnames = ['date', 'pair', 'subject', 'signature', 'classroom', 'classroom_building', 'group_name']
    #writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
    #writer.writeheader()
    response = requests.get(url)
    data = response.json()
    print(f': {response.status_code} ({len(data)})')
    for schedule in data:
        DATEarr=schedule['date'].split('.')
        DATE=str(DATEarr[2]+DATEarr[1]+DATEarr[0])
        #writer.writerow({
        #    'date': schedule['date'].strip(),
        #    'pair': PAIR_TIMES[schedule['pair'].strip()],
        #    'signature': schedule['signature'].strip(),
        #    'classroom': CLASS.strip(),
        #    'classroom_building': schedule['classroom_building'].strip(),
        #    'group_name': schedule['group_name'].strip(),
        #})

        insert_query = """
        INSERT INTO schedule (date, pair, subject, signature, classroom, classroom_building, group_name) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (DATE.strip(), PAIR_TIMES[schedule['pair'].strip()], schedule['subject'].strip(),
                                      schedule['signature'].strip(), schedule['classroom'].strip(),
                                      schedule['classroom_building'].strip(), schedule['group_name'].strip()))

# Подтверждение изменений в базе данных и закрытие соединения
connection.commit()
connection.close()