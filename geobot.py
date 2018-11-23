# -*- coding: utf-8 -*-
from telegram.ext import Updater, CommandHandler, MessageHandler, RegexHandler, Filters, ConversationHandler
from telegram import ReplyKeyboardMarkup, KeyboardButton
import settings
import logging
from utils import find_dist, check_max_dist, check_fix_loc, check_user_position, check_state, check_all, basic_keyboard, chosen_keyboard, fix_keyboard, br_keyboard, find_near
from handlers import *


logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO, filename='bot.log')
max_rad=0


def main():
    mybot = Updater(settings.KEY, request_kwargs=settings.PROXY)
    dp = mybot.dispatcher
    conv = ConversationHandler(
    entry_points=[
        CommandHandler("start", greet_user, pass_user_data=True), 
        RegexHandler("Restart", greet_user, pass_user_data=True)
    ],
    states={
        "Default" : [
            RegexHandler("Зафиксировать координаты", state_fix, pass_user_data=True),
            RegexHandler("Очистить координаты", clear_fix_location, pass_user_data=True),
            RegexHandler("Избранное", state_chosen, pass_user_data=True),
            RegexHandler("Справка", help, pass_user_data=True),
            RegexHandler("Фастфуд", find_type_handler, pass_user_data=True),
            RegexHandler("Банк", find_type_handler, pass_user_data=True),
            RegexHandler("MR", state_max_dist, pass_user_data=True),
            MessageHandler(Filters.text, find_near_handler, pass_user_data=True)
        ],
        "Chosen":[
            RegexHandler("Restart", greet_user, pass_user_data=True), 
            RegexHandler("Add", state_add_chosen, pass_user_data=True),
            RegexHandler("Clear", del_chosen, pass_user_data=True),
            RegexHandler("Get", get_chosen, pass_user_data=True)
        ],
        "Fix":[
            RegexHandler("Restart", greet_user, pass_user_data=True),  
            RegexHandler("Произвольные", state_set_location, pass_user_data=True),
            MessageHandler(Filters.location, fix_user_location, pass_user_data=True)],
        "Add_chosen":[
            RegexHandler("Restart", greet_user, pass_user_data=True), 
            RegexHandler("Назад", state_chosen, pass_user_data=True), 
            MessageHandler(Filters.text, add_to_chosen, pass_user_data=True)],
        "Set_loc":[
            RegexHandler("Restart", greet_user, pass_user_data=True),
            MessageHandler(Filters.text, set_location, pass_user_data=True)],
        "MR":[
            RegexHandler("Restart", greet_user, pass_user_data=True), 
            MessageHandler(Filters.text, set_max_dist, pass_user_data=True)
        ]
    },
    fallbacks=[MessageHandler(Filters.video | Filters.photo, dontknow)]
)
    dp.add_handler(conv)
    dp.add_handler(MessageHandler(Filters.location, user_location, pass_user_data=True, edited_updates=True))
    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()