import telebot
import logging
from telebot import custom_filters, StateMemoryStorage
from django.conf import settings


state_storage = StateMemoryStorage()
bot = telebot.TeleBot(settings.BOT_TOKEN, state_storage=state_storage)

bot.set_webhook(settings.WEBHOOK_URL)


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.IsDigitFilter())
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)
