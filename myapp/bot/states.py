from telebot.handler_backends import State, StatesGroup


class BUDI(StatesGroup):
    add_timezone = State()
    add_geolok = State()
    add_timer = State()
    add_hard_time = State()
    final = State()
    # delete = State()
