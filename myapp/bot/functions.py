from datetime import datetime, timedelta, timezone
from telebot import types
from myapp.models import UserModel, NotesModel
from django.utils import timezone
from timezonefinder import TimezoneFinder
import pytz
from myapp.bot.main import bot
import re
import time
import threading



def check_time_zone(message):
    try:
        user = UserModel.objects.get(user_id=message.from_user.id)
        if user.timezone is not None:
            return 1
        return 0
    except:
        user = UserModel()
        user.user_id = message.from_user.id
        user.username = message.from_user.username
        user.save()
        return 0


def get_timezone_name(lat, lon):
    tf = TimezoneFinder()
    timezone_id = tf.timezone_at(lng=lon, lat=lat)
    tz = pytz.timezone(timezone_id)
    st = str(datetime.now(tz))
    return int(st[26:29])


def time_zone(message):
    try:
        text = int(message.text)
        if text < -12 or text > 14:
            return 'Часовой пояс введен неправильно, попробуйте еще раз'
        else:
            user = UserModel.objects.get(user_id=message.from_user.id)
            user.timezone = text
            user.save()
            return 'Часовой пояс добавлен успешно'
    except ValueError:
        return 'Произошла какая-то ошибка, проверьте формат введенного текста'


def add_notification_timer(message, answer):
    text = message.text
    start_time = datetime.now() + timedelta(minutes=int(answer))
    notes = NotesModel()
    notes.user = message.from_user.id
    notes.text = text
    notes.time = start_time
    href = threading.Timer(int(answer) * 60, timer_expired, args=[message.chat.id, text, start_time, message])
    href.start()
    notes.href_on_timer = href
    notes.save()
    return 'Добавили ваше напоминание!'


def add_notification_hard_time(message, answer):
    text = message.text
    arr1 = parse_date_time(answer)
    day_start = arr1[0]
    month_start = arr1[1]
    year_start = arr1[2]
    hour_start = arr1[3]
    minute_start = arr1[4]
    timer = UserModel.objects.get(user_id=str(message.from_user.id)).timezone - 6
    start_time = (datetime(year_start, month_start, day_start, hour_start, minute_start) -
                  timedelta(hours=timer))
    start_time = start_time.astimezone(timezone.utc)
    time_to_add = start_time
    notes = NotesModel()
    notes.user = message.from_user.id
    notes.text = text
    notes.time = start_time
    timer = UserModel.objects.get(user_id=str(message.from_user.id)).timezone - 3
    start_time = (datetime(year_start, month_start, day_start, hour_start, minute_start) -
                  timedelta(hours=timer))
    start_time = start_time.astimezone(timezone.utc)
    delta_time = start_time - datetime.now(timezone.utc)
    minutes_until_start = delta_time.total_seconds()
    href = threading.Timer(minutes_until_start, timer_expired, args=[message.chat.id, text, time_to_add, message])
    href.start()
    notes.href_on_timer = href
    notes.save()
    return 'Добавили ваше напоминание!'


def timer_expired(chat_id, text, start_time, message):
    note = NotesModel.objects.get(user=message.from_user.id,
                                  time=start_time,
                                  text=text)
    note.delete()
    bot.send_message(chat_id,
                     f'Мой будильник сходит с ума, когда я сплю, кхм....\n'
                     f'Время вышло, ваше напоминание:\n{text}')


def parse_date_time(date_time_str):
    numbers = re.split(r'[ .:]+', date_time_str)
    numbers = [int(num) for num in numbers]
    return numbers

#
# def cancel_timer(text):
#     if timer is not None and timer.is_alive():
#         timer.cancel()
