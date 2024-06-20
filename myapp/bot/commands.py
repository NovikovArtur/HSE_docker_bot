import myapp
from myapp.bot.main import bot
from myapp.models import UserModel, NotesModel
import myapp.bot.functions as func
import myapp.bot.keyboards as key
from myapp.bot.states import BUDI


@bot.message_handler(commands=['start'])
def send_start(message):
    bot.delete_state(message.from_user.id, message.chat.id)
    try:
        UserModel.objects.get(user_id=message.from_user.id)
    except myapp.models.UserModel.DoesNotExist:
        user = UserModel()
        user.user_id = message.from_user.id
        user.username = message.from_user.username
        user.save()
    if message.chat.id < 0:
        bot.send_message(message.chat.id, "Привет!\nЯ - бот будильник и я помогу вам не забыть что-то важное\n"
                                          "Пока я работаю только в личных сообщениях(\nЖду тебя там!")
    else:
        if func.check_time_zone(message) == 0:
            bot.send_message(message.chat.id, "Привет!\nРад, что я тебе понравился!)\nТак как я работаю в "
                                              "разных странах, мне необходимо узнать твой часовой пояс")
            bot.send_message(message.chat.id,
                             "Выберите ваш часовой пояс относительно UTC или отправьте "
                             "геопозицию для автоматического определения. Если предложенные"
                             " варианты не подходят, укажите ваш часовой пояс самостоятельно."
                             " Пример (МСК): +3",
                             reply_markup=key.type_timezone)
            bot.set_state(message.from_user.id, BUDI.add_timezone, message.chat.id)
        else:
            bot.send_message(message.chat.id,
                             "Приветствую тебя в главном меню!\nЗдесь ты можешь создать напоминание или узнать "
                             "информацию об авторах",
                             reply_markup=key.keyboard_main_menu)


@bot.message_handler(commands=['change_timezone'])
def send_start(message):
    bot.delete_state(message.from_user.id, message.chat.id)
    try:
        UserModel.objects.get(user_id=message.from_user.id)
    except myapp.models.UserModel.DoesNotExist:
        user = UserModel()
        user.user_id = message.from_user.id
        user.username = message.from_user.username
        user.save()
    if message.chat.id < 0:
        bot.send_message(message.chat.id, "Это команда работает только в личных сообщениях с ботом(")
    else:
        bot.send_message(message.chat.id,
                         "Выберите ваш часовой пояс относительно UTC или отправьте "
                         "геопозицию для автоматического определения. Если предложенные"
                         " варианты не подходят, укажите ваш часовой пояс самостоятельно."
                         " Пример (МСК): +3",
                         reply_markup=key.type_timezone)
        bot.set_state(message.from_user.id, BUDI.add_timezone, message.chat.id)


@bot.message_handler(commands=['see_timer'])
def send_all_timers(message):
    bot.delete_state(message.from_user.id, message.chat.id)
    try:
        UserModel.objects.get(user_id=message.from_user.id)
    except myapp.models.UserModel.DoesNotExist:
        user = UserModel()
        user.user_id = message.from_user.id
        user.username = message.from_user.username
        user.save()
    if message.chat.id < 0:
        bot.send_message(message.chat.id, "Это команда работает только в личных сообщениях с ботом(")
    else:
        all_timers = NotesModel.objects.filter(user=message.from_user.id)
        text = 'Ваши установленные напоминалки:\n'
        for i in all_timers:
            time = str(i.time)
            text += f"{i.id}   {i.text}   {time[0:19]}\n"
        bot.send_message(message.chat.id, text, reply_markup=key.back_to_menu)
        # bot.set_state(message.from_user.id, BUDI.delete, message.chat.id)


# @bot.message_handler(commands=['send'])
# def send_message(message):
#     bot.delete_state(message.from_user.id, message.chat.id)
#     try:
#         UserModel.objects.get(user_id=message.from_user.id)
#     except myapp.models.UserModel.DoesNotExist:
#         user = UserModel()
#         user.user_id = message.from_user.id
#         user.username = message.from_user.username
#         user.save()
#     if message.chat.id < 0:
#         bot.send_message(message.chat.id, "Это команда работает только в личных сообщениях с ботом(")
#     else:
#         bot.send_message(message.chat.id,
#                          "Напиши id пользователя, которому хочешь отправить соо",
#                          reply_markup=key.back_to_menu)
#         bot.set_state(message.from_user.id, BUDI.delete, message.chat.id)
