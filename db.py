import sqlite3
from datetime import datetime
import constants


# обновление / добавление нового пользователя
def update_user(id, profile):
    conn = sqlite3.connect('users.sqlite3')
    curs = conn.cursor()
    curs.execute("SELECT `id` FROM `users` WHERE `telegram_id` = " + str(id))
    res = curs.fetchall()
    if not res:
        curs.execute("INSERT INTO `users` (telegram_id, profile) VALUES (" + str(id) + ", '" + str(profile) + "')")
        conn.commit()
    else:
        curs.execute("UPDATE `users` SET `profile` = '" + str(profile) + "' WHERE `telegram_id` = " + str(id))
        conn.commit()
    conn.close()


# получение профиля(класса) пользователя
def get_schedule_user(id):
    conn = sqlite3.connect('users.sqlite3')
    curs = conn.cursor()
    curs.execute("SELECT `profile` FROM `users` WHERE `telegram_id` = " + str(id))
    res = curs.fetchall()
    conn.close()
    return res[0][0]


# получить массив список сегодняшних предметов для данного профиля
def get_today_schedule(profile):
    current_day = datetime.weekday(datetime.now())
    if current_day == 7:
        return constants.schedule[profile]['mon']
    elif current_day == 1:
        return constants.schedule[profile]['tue']
    elif current_day == 2:
        return constants.schedule[profile]['wen']
    elif current_day == 3:
        return constants.schedule[profile]['thu']
    elif current_day == 4:
        return constants.schedule[profile]['fri']
    elif current_day == 5:
        return constants.schedule[profile]['sat']
    else:
        return ['Сегодня нет уроков!']


# получить следующий / текущий предмет для данного профиля
def get_now_lesson(profile):
    current_day = datetime.weekday(datetime.now())
    day = ''
    if current_day == 7:
        day = 'mon'
    elif current_day == 1:
        day = 'tue'
    elif current_day == 2:
        day = 'wed'
    elif current_day == 3:
        day = 'thu'
    elif current_day == 4:
        day = 'fri'
    elif current_day == 5:
        day = 'sat'
    else:
        day = 'sun'
    now = datetime.now()
    hour = now.hour
    minute = now.minute

    current_lesson_time = 0
    if hour == 8 and minute >= 30 or hour == 9 and minute <= 10:
        current_lesson_time = 0
    if hour == 9 and minute > 10:
        current_lesson_time = 1
    if hour == 10:
        current_lesson_time = 2
    if hour == 11:
        current_lesson_time = 3
    if hour == 12:
        current_lesson_time = 4
    if hour == 13 and 0 <= minute <= 50:
        current_lesson_time = 5
    if hour == 13 and minute > 50 or hour == 14 and minute <= 40:
        current_lesson_time = 6
    if hour == 14 and minute > 40 or hour > 14:
        current_lesson_time = 7

    if len(constants.schedule[profile][day]) < current_lesson_time:
        return 'Поздравляю, у тебя кончились уроки!'
    else:
        return constants.schedule[profile][day][current_lesson_time]
