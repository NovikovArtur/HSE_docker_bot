from telebot import types
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


type_timezone = InlineKeyboardMarkup()
for i in range(-12, 12, 5):
    btn1 = InlineKeyboardButton(str(i),
                                callback_data=str(i))
    btn2 = InlineKeyboardButton(str(i+1),
                                callback_data=str(i+1))
    btn3 = InlineKeyboardButton(str(i+2),
                                callback_data=str(i+2))
    btn4 = InlineKeyboardButton(str(i + 3),
                                callback_data=str(i+3))
    btn5 = InlineKeyboardButton(str(i + 4),
                                callback_data=str(i+4))
    type_timezone.row(btn1, btn2, btn3, btn4, btn5)
btn1 = InlineKeyboardButton(str(13),
                            callback_data=str(13))
btn2 = InlineKeyboardButton(str(14),
                            callback_data=str(14))
type_timezone.row(btn1, btn2)
type_timezone.row(InlineKeyboardButton("С помощью геолокации",
                                       callback_data="С помощью геолокации"))
type_timezone.row(InlineKeyboardButton("Текстом",
                                       callback_data="Текстом"))


keyboard_main_menu = types.InlineKeyboardMarkup()
keyboard_main_menu.add(types.InlineKeyboardButton(text="Добавить новое напоминание",
                                                  callback_data="Добавить новое напоминание"))
keyboard_main_menu.add(types.InlineKeyboardButton(text="Об авторах",
                                                  callback_data="Об авторах"))


back_to_menu = types.InlineKeyboardMarkup()
back_to_menu.add(types.InlineKeyboardButton(text="К главному меню",
                                            callback_data="К главному меню"))


choose_method = types.InlineKeyboardMarkup()
choose_method.add(types.InlineKeyboardButton(text="Поставить таймер",
                                             callback_data="Поставить таймер"))
choose_method.add(types.InlineKeyboardButton(text="Завести будильник",
                                             callback_data="Завести будильник"))
choose_method.add(types.InlineKeyboardButton(text="К главному меню",
                                             callback_data="К главному меню"))

