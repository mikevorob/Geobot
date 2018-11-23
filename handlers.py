from utils import find_dist, check_max_dist, check_fix_loc, check_user_position, check_state, check_all, basic_keyboard, chosen_keyboard, fix_keyboard, br_keyboard, find_near, find_near_type
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from yandex_geocoder import Client
import yandex_geocoder
from datetime import datetime
import math
import db2
from db2 import Branches, Users
from yandex_geocoder import Client
from sqlalchemy import update
from help import content

def greet_user(bot, update, user_data):
    chat_id=update.message.chat.id
    count=len(Users.query.filter(Users.cid==chat_id).all())
    if count==0:
        user=Users(cid=chat_id, chosen='')
        db2.db_session.add(user)
        db2.db_session.commit()
    text = 'Вызван /start'
    check_all(user_data)
    if not user_data['user_position'] and not user_data['fixed_location']:
        user_data['state']='Default; нет координат'
    elif user_data['fixed_location']:
        user_data['state']='Default; фиксированные координаты'
    else:
        user_data['state']='Default; отслеживание'
    basic_keyboard(bot, update, user_data)
    return "Default"



def get_chosen(bot, update, user_data):
    check_all(user_data)
    chat_id=update.message.chat.id
    user=Users.query.filter(Users.cid==chat_id).first()
    if user.chosen=='':
        update.message.reply_text("Список избранного пуст")
    else:
        chosen_list=user.chosen.split('; ')
        for point in chosen_list:
            dist=find_near(point, user_data)
            if not(dist):
                update.message.reply_text("В пределах {} м {} не обнаружен".format(user_data['max_dist'], point))
            else:
                update.message.reply_text("Ближайший {} находится по адресу {}; Расстояние {:.2f} метров".format (point, dist[0], dist[1]))
    if not user_data['user_position'] and not user_data['fixed_location']:
        user_data['state']='Default; нет координат'
    elif user_data['fixed_location']:
        user_data['state']='Default; фиксированные координаты'
    else:
        user_data['state']='Default; отслеживание'
    basic_keyboard(bot, update, user_data)
    return "Default"


def user_location(bot, update, user_data):
    check_all(user_data)
    flag=1
    if not user_data["user_position"]:
        flag=0
    msg=None
    if update.edited_message:
        msg = update.edited_message
    else:
        msg = update.message       
    print ('{}    {}'.format(msg.location, datetime.now()))
    user_data['user_position']={'longitude' : msg.location.longitude, 'latitude' : msg.location.latitude}
    print(user_data)
    if flag==0 and not user_data["fixed_location"]:
        cur_coord_state="отслеживание"
        cur_state=user_data['state'].split('; ')[0]
        user_data["state"]="{}; {}".format(cur_state, cur_coord_state)
        basic_keyboard(bot, update, user_data)
        


def help(bot, update, user_data):
    update.message.reply_text(content)


def set_radius (bot, update, user_data):
    user_text = update.message.text
    user_list=user_text.split(' ')
    check_max_dist(user_data)
    user_data['max_dist']=float(user_list[1])


def fix_user_location (bot, update, user_data):
    check_all(user_data)
    user_data['fixed_location']=update.message.location
    if not user_data['user_position'] and not user_data['fixed_location']:
        user_data['state'] = 'Fix; нет координат'
    elif user_data['fixed_location']:
        user_data['state'] = 'Fix; фиксированные координаты'
    else:
        user_data['state'] = 'Fix; отслеживание'
    fix_keyboard(user_data)
    return "Fix"


def clear_fix_location(bot, update, user_data):
    check_all(user_data)
    user_data['fixed_location'] = []
    if not user_data['user_position'] and not user_data['fixed_location']:
        user_data['state']='Default; нет координат'
    elif user_data['fixed_location']:
        user_data['state']='Default; фиксированные координаты'
    else:
        user_data['state']='Default; отслеживание'
    basic_keyboard(user_data)
    return "Default"


def set_location(bot, update, user_data):
    try:
        check_all(user_data)
        user_text = update.message.text
        addr = user_text
        coord=Client.coordinates(addr)
        user_data['fixed_location']  = {'longitude' : float(coord[0]), 'latitude' : float(coord[1])}
        if not user_data['user_position'] and not user_data['fixed_location']:
            user_data['state'] = 'Fix; нет координат'
        elif user_data['fixed_location']:
            user_data['state'] = 'Fix; фиксированные координаты'
        else:
            user_data['state'] = 'Fix; отслеживание'
        fix_keyboard(bot, update, user_data)
        return "Fix"
    except yandex_geocoder.exceptions.YandexGeocoderAddressNotFound:
        update.message.reply_text("Неверный адрес")
        update.message.reply_text("Введите верный адрес или Restart")
        return "Set_loc"


def del_chosen(bot, update, user_data):
    chat_id=update.message.chat.id
    user=Users.query.filter(Users.cid == chat_id).first()
    user.chosen = ''
    db2.db_session.commit()
    return "Chosen"


def find_near_handler(bot, update, user_data):
    check_all(user_data)
    str1 = update.message.text
    dist = find_near(str1, user_data)
    if not(dist):
        update.message.reply_text("В пределах {} м {} не обнаружен".format(user_data['max_dist'], str1))
    else:
        update.message.reply_text("Ближайший {} находится по адресу {}; Расстояние {:.2f} метров".format (str1, dist[0], dist[1]))
    basic_keyboard(bot, update, user_data)
    return "Default"


def state_fix(bot, update, user_data):
    check_all(user_data)
    if not user_data['user_position'] and not user_data['fixed_location']:
        user_data['state'] = 'Fix; нет координат'
    elif user_data['fixed_location']:
        user_data['state'] = 'Fix; фиксированные координаты'
    else:
        user_data['state'] = 'Fix; отслеживание'
    fix_keyboard(bot, update, user_data)
    return "Fix"


def state_chosen(bot, update, user_data):
    check_all(user_data)
    if not user_data['user_position'] and not user_data['fixed_location']:
        user_data['state'] = 'Chosen; нет координат'
    elif user_data['fixed_location']:
        user_data['state'] = 'Chosen; фиксированные координаты'
    else:
        user_data['state'] = 'Chosen; отслеживание'
    chosen_keyboard(bot, update, user_data)
    return "Chosen"


def state_add_chosen(bot, update, user_data):
    check_all(user_data)
    br_keyboard(bot, update, user_data)
    return "Add_chosen"


def state_set_location(bot, update, user_data):
    check_all(user_data)
    text="Введите адрес"
    reply_markup = ReplyKeyboardRemove()
    bot.sendMessage(chat_id=update.message.chat.id, text=text, reply_markup=reply_markup)
    return "Set_loc"


def state_max_dist(bot, update, user_data):
    check_all(user_data)
    text = "Введите максимально допустимое расстояние"
    reply_markup = ReplyKeyboardRemove()
    bot.sendMessage(chat_id=update.message.chat.id, text=text, reply_markup=reply_markup)
    return "MR"


def set_max_dist(bot, update, user_data):
    check_all(user_data)
    user_text = update.message.text
    try:
        user_data['max_dist'] = int(user_text)
        if not user_data['user_position'] and not user_data['fixed_location']:
            user_data['state'] = 'Default; нет координат'
        elif user_data['fixed_location']:
            user_data['state'] = 'Default; фиксированные координаты'
        else:
            user_data['state'] = 'Default; отслеживание'
        basic_keyboard(bot, update, user_data)
        return "Default"
    except ValueError:
        update.message.reply_text("Расстояние должно быть целым числом")
        update.message.reply_text("Введите целое число или Restart")
        return "max_dist"


def add_to_chosen(bot, update, user_data):
    user_text=update.message.text
    chat_id=update.message.chat.id
    user=Users.query.filter(Users.cid==chat_id).first()
    if user.chosen=='':
        user.chosen=user_text
        db2.db_session.commit()
    else:
        chosen_list=user.chosen.split('; ')
        if not (user_text in chosen_list):
            user.chosen="{}; {}".format(user.chosen, user_text)
            db2.db_session.commit()


def find_type_handler (bot,update, user_data):
    str1 = update.message.text
    if str1 == "Фастфуд":
        type_name = 'food'
    if str1 == "Банк":
        type_name = 'bank'
    dist = find_near_type(type_name, user_data)
    if not(dist):
        update.message.reply_text("В пределах {} м {} не обнаружен".format(user_data['max_dist'], str1))
    else:
        update.message.reply_text("Ближайший {} находится по адресу {}; Расстояние {:.2f} метров".format (str1, dist[0], dist[1]))
    basic_keyboard(bot, update, user_data)
    return "Default"


def dontknow(bot, update):
    update.message.reply_text("Некорректный тип данных")