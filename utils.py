import math
import db2
from db2 import Branches
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, KeyboardButton

def find_dist(target_loc, user_data):
    check_all(user_data)
    if not user_data['fixed_location']:
        user_loc1=user_data['user_position']
    else:
        user_loc1=user_data['fixed_location']
    user_lat = user_loc1['latitude']*math.pi/180
    user_lon = user_loc1['longitude']*math.pi/180
    target_lat = float(target_loc[1])*math.pi/180
    target_lon = float(target_loc[0])*math.pi/180
    cosd = math.sin(user_lat) * math.sin(target_lat) + math.cos(user_lat) * math.cos(target_lat) * math.cos(user_lon - target_lon)
    d = math.acos(cosd)
    R = 6371302
    dist = d * R
    return dist


def check_max_dist(user_data):
    if (not 'max_dist' in user_data):
        user_data['max_dist'] = 0


def check_fix_loc(user_data):
    if (not 'fixed_location' in user_data):
        user_data['fixed_location'] = []


def check_user_position(user_data):
    if (not 'user_position' in user_data):
        user_data['user_position'] = {}


def check_state(user_data):
    if (not 'state' in user_data):
        user_data['state'] = ''


def check_all(user_data):
    check_state(user_data)
    check_user_position(user_data)
    check_fix_loc(user_data)
    check_max_dist(user_data)

def basic_keyboard(bot, update, user_data):
    text='Default'
    check_all
    my_keyboard = ReplyKeyboardMarkup([[user_data['state'], 'Restart','MR'],['Зафиксировать координаты', 'Очистить координаты', 'Избранное', 'Справка'],['Фастфуд', 'Банк'],['KFC', "McDonald's", 'Burger King'],['Сбербанк', 'Росбанк', 'Банк Русский Стандарт']])
    update.message.reply_text(text, reply_markup=my_keyboard)


def chosen_keyboard(bot, update, user_data):
    text='Chosen'
    check_all
    my_keyboard = ReplyKeyboardMarkup([[user_data['state'], 'Restart'],['Get','Add','Clear']])
    update.message.reply_text(text, reply_markup=my_keyboard)


def fix_keyboard(bot, update, user_data):
    text='Fix'
    check_all
    fix_btn=KeyboardButton("Текущие", request_location=True)
    my_keyboard = ReplyKeyboardMarkup([[user_data["state"], 'Restart'],[fix_btn,'Произвольные','Clear']])
    update.message.reply_text(text, reply_markup=my_keyboard)


def br_keyboard(bot, update, user_data):
    text='Branches'
    my_keyboard = ReplyKeyboardMarkup([['Назад','Restart'],['KFC', "McDonald's", 'Burger King'],['Сбербанк', 'Росбанк', 'Банк Русский Стандарт']])
    update.message.reply_text(text, reply_markup=my_keyboard)


def find_near(str1, user_data):
    min_dist =100000000
    check_max_dist(user_data)
    max_rad=user_data['max_dist']
    for line in Branches.query.filter(Branches.Type==str1).all():
        loc = [line.lon, line.lat]
        cur_dist = find_dist(loc, user_data)
        if (min_dist == None or cur_dist < min_dist):
            min_dist = cur_dist
            addr=line.address
    if min_dist <= max_rad or max_rad == 0:
        return [addr, min_dist]
    else:
        return []


def find_near_type(str1, user_data):
    min_dist = None
    check_max_dist(user_data)
    max_rad=user_data['max_dist']
    for line in Branches.query.filter(Branches.Type2==str1).all():
        loc = [line.lon, line.lat]
        cur_dist = find_dist(loc, user_data)
        if (min_dist == None or cur_dist < min_dist):
            min_dist = cur_dist
            addr=line.address
    if min_dist <= max_rad or max_rad == 0:
        return [addr, min_dist]
    else:
        return []