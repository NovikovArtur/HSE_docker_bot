from telebot import types
from myapp.bot.main import bot
from myapp.models import UserModel, NotesModel
import myapp.bot.functions as func
import myapp.bot.keyboards as key
from myapp.bot.states import BUDI
import myapp.bot.commands as com
from telebot import apihelper
import time
from datetime import datetime

hideBoard = types.ReplyKeyboardRemove()


@bot.callback_query_handler(lambda call: True, state=BUDI.add_timezone)
def change_timezone_state(callback: types.CallbackQuery):
    bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                  reply_markup=None)
    if str(callback.data) == 'С помощью геолокации':
        try:
            user = UserModel.objects.get(user_id=callback.from_user.id)
            user.timezone = None
            user.save()
        except UserModel.DoesNotExists:
            user = UserModel()
            user.user_id = callback.from_user.id
            user.username = callback.from_user.username
            user.save()
        send_timezone = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn1 = types.KeyboardButton("Отправить местоположение", request_location=True)
        send_timezone.add(btn1)
        bot.send_message(callback.message.chat.id,
                         "Нажмите на кнопку отправить местоположение, чтобы мы могли определить ваш"
                         " часовой пояс", reply_markup=send_timezone)
        bot.set_state(callback.from_user.id, BUDI.add_geolok, callback.message.chat.id)
    elif str(callback.data) == 'Текстом':
        try:
            user = UserModel.objects.get(user_id=callback.from_user.id)
            user.timezone = None
            user.save()
        except UserModel.DoesNotExists:
            user = UserModel()
            user.user_id = callback.from_user.id
            user.username = callback.from_user.username
            user.save()
        bot.send_message(callback.message.chat.id, "Напишите ваш часовой пояс.\nПример:\n-3")
        bot.set_state(callback.from_user.id, BUDI.add_geolok, callback.message.chat.id)
    else:
        try:
            user = UserModel.objects.get(user_id=callback.from_user.id)
            user.timezone = callback.data
            user.save()
        except UserModel.DoesNotExists:
            user = UserModel()
            user.user_id = callback.from_user.id
            user.username = callback.from_user.username
            user.timezone = callback.data
            user.save()
        bot.send_message(chat_id=callback.message.chat.id,
                         text='Часовой пояс успешно добавлен!',
                         reply_markup=key.keyboard_main_menu)
        bot.delete_state(callback.from_user.id, callback.message.chat.id)


@bot.message_handler(content_types=['location'], state=BUDI.add_geolok)
def add_timezone_state(message: types.Message):
    bot.send_message(message.chat.id,
                     'Добавляем часовой пояс',
                     reply_markup=hideBoard)
    latitude = message.location.latitude
    longitude = message.location.longitude
    tz_name = func.get_timezone_name(latitude, longitude)
    user = UserModel.objects.get(user_id=message.from_user.id)
    user.timezone = tz_name
    user.save()
    bot.send_message(chat_id=message.chat.id,
                     text='Часовой пояс добавлен успешно!',
                     reply_markup=key.keyboard_main_menu)
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(state=BUDI.add_geolok)
def add_timezone_text_state(message: types.Message):
    bot.send_message(message.chat.id,
                     'Добавляем часовой пояс',
                     reply_markup=hideBoard)
    text = func.time_zone(message)
    if text == ('Часовой пояс введен неправильно, попробуйте еще раз' or
                'Произошла какая-то ошибка, проверьте формат введенного текста'):
        bot.send_message(chat_id=message.chat.id,
                         text=text)
        bot.delete_state(message.from_user.id, message.chat.id)
        com.send_start(message)
    else:
        bot.send_message(chat_id=message.chat.id,
                         text='Часовой пояс успешно добавлен!',
                         reply_markup=key.keyboard_main_menu)
        bot.delete_state(message.from_user.id, message.chat.id)


@bot.callback_query_handler(lambda callback: callback.data == 'Об авторах')
def about_authors(callback: types.CallbackQuery):
    bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                  reply_markup=None)
    bot.send_message(callback.message.chat.id,
                     "Меня разработал прекрасный писатель ботов Новиков Артур из HSE, который очень хочет получить"
                     " 10 баллов за меня, хехехеххе",
                     reply_markup=key.back_to_menu)


@bot.callback_query_handler(lambda callback: callback.data == 'К главному меню')
def main_menu(callback: types.CallbackQuery):
    bot.delete_state(callback.from_user.id, callback.message.chat.id)
    bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                  reply_markup=None)
    bot.send_message(callback.message.chat.id,
                     "Приветствую тебя в главном меню!\nЗдесь ты можешь создать напоминание или узнать "
                     "информацию об авторах",
                     reply_markup=key.keyboard_main_menu)


@bot.callback_query_handler(lambda callback: callback.data == 'Добавить новое напоминание')
def create_new_notification(callback: types.CallbackQuery):
    bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                  reply_markup=None)
    bot.send_message(callback.message.chat.id,
                     "Выбери, как ты хочешь добавить уведомление: через некоторое количество минут "
                     "или в определенное время",
                     reply_markup=key.choose_method)


@bot.callback_query_handler(lambda callback: callback.data == 'Поставить таймер')
def set_timer(callback: types.CallbackQuery):
    bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                  reply_markup=None)
    bot.send_message(callback.message.chat.id,
                     "Введи время в минутах через которое я тебе напомню то что ты хочешь")
    bot.set_state(callback.from_user.id, BUDI.add_timer, callback.message.chat.id)


@bot.callback_query_handler(lambda callback: callback.data == 'Завести будильник')
def set_timer(callback: types.CallbackQuery):
    bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                  reply_markup=None)
    bot.send_message(callback.message.chat.id,
                     "Напишите дату в которую хочешь увидеть напоминание в формате:\nДД.ММ.ГГГГ ЧЧ:ММ"
                     "\nПример:\n17.03.2024 19:53")
    bot.set_state(callback.from_user.id, BUDI.add_timer, callback.message.chat.id)


@bot.message_handler(state=BUDI.add_timer)
def add_timer(message: types.Message):
    answer = str(message.text)
    user = UserModel.objects.get(user_id=message.from_user.id)
    user.answer = answer
    user.save()
    if ':' in answer:
        bot.send_message(message.chat.id,
                         f"Сохранили ваше время!\nНапомним вам в {answer}. Стоп....\n"
                         f"А что напомнить.....\nНапишите текст сообщения, о котором бы хотели бы получить "
                         f"напоминание")
    else:
        bot.send_message(message.chat.id,
                         f"Сохранили ваше время!\nНапомним вам через {answer} минут. Стоп....\n"
                         f"А что напомнить.....\nНапишите текст сообщения, о котором бы хотели бы получить "
                         f"напоминание")
    bot.set_state(message.from_user.id, BUDI.final, message.chat.id)


@bot.message_handler(state=BUDI.final)
def add_hard_time(message: types.Message):
    user = UserModel.objects.get(user_id=message.from_user.id)
    answer = user.answer
    try:
        text = func.add_notification_timer(message, answer)
        bot.send_message(message.chat.id,
                         text,
                         reply_markup=key.keyboard_main_menu)
    except:
        try:
            text = func.add_notification_hard_time(message, answer)
            bot.send_message(message.chat.id,
                             text,
                             reply_markup=key.keyboard_main_menu)
        except:
            bot.send_message(message.chat.id, "Что-то пошло не так(", reply_markup=key.keyboard_main_menu)
    bot.delete_state(message.from_user.id, message.chat.id)


# @bot.message_handler(state=BUDI.delete)
# def delete(message: types.Message):
#     func.cancel_timer(message.text)
#     bot.send_message(message.chat.id, "Таймер удален", reply_markup=key.keyboard_main_menu)
#     bot.delete_state(message.from_user.id, message.chat.id)
