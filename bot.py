import telebot
from telebot import types

import api_service
from ImageParser import *
import here_api_service
import datetime

BOT_TOKEN = ''
ERROR_MESSAGE = 'Произошла непредвиденная ошибкаю Попробуйте ещё разок'
IMG_SEARCH_ERROR_MESSAGE = 'Не удалось найти товар с картинки'
TEXT_SEARCH_ERROR_MESSAGE = 'Ничего не найдено. Возможно, товар закончился или в запросе допущена ошибка. ' \
                            'Нужна помощь - напиши /help'
ADD_TO_BASKET_MESSAGE = 'Товар добавлен в корзину'
ADD_TO_BASKET_ERROR_MESSAGE = 'Выбранный товар недоступен'
REMOVE_FROM_BASKET_MESSAGE = 'Товар удалён из корзины'
MAKE_ORDER_MESSAGE = 'Заказ оформлен'
HELP_TEXT = 'Напиши название или скинь фото упоковки, ' \
            'а я попробую найти выгодные предложения для тебя.\n' \
            'Чтобы посмтореть корзину, отправь мне /basket' \


bot = telebot.TeleBot(BOT_TOKEN)


def send_result(message, results):
    for p in results:
        keyboard = types.InlineKeyboardMarkup()
        remove_btn = types.InlineKeyboardButton(text="Добавить", callback_data="add_{0}".format(p['id']))
        keyboard.add(remove_btn)
        try:
            expires = datetime.datetime.strptime(p['expires'], '%Y-%m-%d').strftime("%d %b %y")
        except:
            expires = 'нет данных'
        text = "*{0}₽* {1}\n{2}\nГоден до: {3}".format(p['price'], p['name'], p['manufacturer'], expires)
        bot.send_message(message.from_user.id, text, reply_markup=keyboard, parse_mode='Markdown')


def send_location_btn(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
    keyboard.add(button_geo)
    bot.send_message(message.chat.id, "Нажмите на кнопку, чтобы передать местоположение", reply_markup=keyboard)


@bot.message_handler(commands=['start', 'go'])
def start_handler(message):
    bot.send_message(message.chat.id, 'Привет, я бот для заказа лекарств. ' + HELP_TEXT)


@bot.message_handler(commands=['help'])
def start_handler(message):
    bot.send_message(message.chat.id, HELP_TEXT)


@bot.message_handler(content_types=['location'])
def handle_loc(message):
    res = here_api_service.find_pharmacies(message.location.latitude, message.location.longitude)
    text = '\n'.join(map(lambda x: "{0} - {1}, {2} м".format(x[0], x[1], x[2]), res))
    text = "Аптеки рядом:\n" + text
    bot.send_message(message.from_user.id, text)


@bot.message_handler(commands=["add"])
def add(message):
    try:
        product_id = int(message.text.replace("/add ", ""))
        result = api_service.add_to_basket(message.from_user.id, product_id)
        if result:
            bot.send_message(message.from_user.id, ADD_TO_BASKET_MESSAGE)
            products = api_service.get_basket(message.from_user.id)
            total_sum = 0
            text = ''
            if products:
                for p in products:
                    total_sum += p['price']
                    text += "*{0}* {1}\n".format(p['price'], p['name'])

            text += "\nОбщая сумма: {0}".format(total_sum)
            text = "Товары в корзине:\n" + text
            bot.send_message(message.from_user.id, text)
        else:
            bot.send_message(message.from_user.id, ADD_TO_BASKET_ERROR_MESSAGE, parse_mode='Markdown')
    except Exception as e:
        bot.send_message(message.from_user.id, ERROR_MESSAGE)


@bot.message_handler(commands=["basket"])
def basket(message):
    try:
        products = api_service.get_basket(message.from_user.id)
        total_sum = 0
        if products:
            for p in products:
                total_sum += p['price']
                keyboard = types.InlineKeyboardMarkup()
                remove_btn = types.InlineKeyboardButton(text="Удалить", callback_data="remove_{0}".format(p['id']))
                keyboard.add(remove_btn)
                text = "{0}\nЦена:{1}\n\n".format(p['name'], p['price'])
                bot.send_message(message.from_user.id, text, reply_markup=keyboard)

            text = "\nОбщая сумма: {0}".format(total_sum)
            keyboard = types.InlineKeyboardMarkup()
            make_order_btn = types.InlineKeyboardButton(text="Оформить заказ", callback_data="make_order")
            keyboard.add(make_order_btn)
            bot.send_message(message.from_user.id, text, reply_markup=keyboard)
        else:
            bot.send_message(message.from_user.id, "Корзина пуста")
    except Exception as e:
        bot.send_message(message.from_user.id, ERROR_MESSAGE)


@bot.message_handler(commands=["remove"])
def remove(message):
    try:
        product_id = int(message.text.replace("/remove ", ""))
        api_service.remove_from_basket(message.from_user.id, product_id)
        bot.send_message(message.from_user.id, REMOVE_FROM_BASKET_MESSAGE)
    except:
        bot.send_message(message.from_user.id, ERROR_MESSAGE)


@bot.message_handler(commands=["make_order"])
def make_order(message):
    try:
        api_service.make_order(message.from_user.id)
        bot.send_message(message.from_user.id, MAKE_ORDER_MESSAGE)
    except:
        bot.send_message(message.from_user.id, ERROR_MESSAGE)


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        file_info = bot.get_file(message.photo[-1].file_id)
        img_data = bot.download_file(file_info.file_path)
        words = get_words_from_image(img_data)
        results = api_service.search_by_words(sorted(words))
        if results:
            send_result(message, results)
        else:
            bot.send_message(message.from_user.id, IMG_SEARCH_ERROR_MESSAGE)
    except:
        bot.send_message(message.from_user.id, ERROR_MESSAGE)


@bot.message_handler(content_types=["text"])
def handle_text(message):
    try:
        if 'аптек' in message.text.lower():
            send_location_btn(message)
            return
        results = api_service.search(message.text)
        if results:
            send_result(message, results)
        else:
            bot.send_message(message.from_user.id, TEXT_SEARCH_ERROR_MESSAGE)
    except Exception as e:
        bot.send_message(message.from_user.id, ERROR_MESSAGE)


@bot.callback_query_handler(func=lambda call: call.data == 'make_order')
def query_text(message):
    make_order(message)
    bot.edit_message_reply_markup(message.from_user.id, message_id=message.message.message_id, reply_markup='')


@bot.callback_query_handler(func=lambda call: call.data.startswith("remove_"))
def query_text(message):
    product_id = message.data.split('_')[1]
    message.message.text = product_id
    api_service.remove_from_basket(message.from_user.id, product_id)
    bot.send_message(message.from_user.id, REMOVE_FROM_BASKET_MESSAGE)
    bot.edit_message_reply_markup(message.from_user.id, message_id=message.message.message_id, reply_markup='')


@bot.callback_query_handler(func=lambda call: call.data.startswith("add_"))
def query_text(message):
    product_id = message.data.split('_')[1]
    message.message.text = product_id
    message.message.from_user.id = message.from_user.id
    add(message.message)


bot.polling(none_stop=True)
