# импортируем библиотеки
import re

import aiogram
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from yarl import URL

from urllib.parse import urlparse

def is_url(url):
  try:
    result = urlparse(url)
    return all([result.scheme, result.netloc])
  except ValueError:
    return False

# id стикеров для приветствия
hello_stickers = ['CAACAgIAAxkBAAEEcyJiVZ0sqQenNM6ER3msbikbMsJQRQACjQgAAnlc4gk0y_uYceajxCME',
                  'CAACAgIAAxkBAAEEcyRiVZ05qVBBZCZWl2vJqtB29m2c3wACuAIAAi8P8AZAVAABvGPVXi0jBA',
                  'CAACAgIAAxkBAAEEcyZiVZ0_fXCHKi8LKFy8D9toFATobAAC2BAAAtdt6ElpkxDUVhg6hiME',
                  'CAACAgIAAxkBAAEEcyhiVZ1N7g-hvCcLGlMrv79yYL307wACkQ8AAo7aAAFIhPeRyUFm2n4jBA',
                  'CAACAgIAAxkBAAEEc8JiVblNOQjWQwi-AAFpfpsCV2qI0-gAAt0IAAIvD_AGmMS8ln43Y24jBA']
# id стикеров для прощания
bye_stickers = ['CAACAgIAAxkBAAEEc7ZiVbi1fX8ZQTbxqCqQedyR3D6VbwACiQgAAnlc4gno718mBrqFJCME',
                'CAACAgIAAxkBAAEEc7hiVbkGZZLQnFJTu10mut7vuleOQAACdg8AAkBRQUh9kH8FliezaSME',
                'CAACAgIAAxkBAAEEc7xiVbktrhcTsMo1HUGqEhCSgJnw4gAC7hYAAqM8sUoj812lcIro3SME',
                'CAACAgIAAxkBAAEEc8RiVblXkMSCYLF4Cg-k0USm0kQnFQACwgIAAi8P8AYM1RNBJvF3CyME']


def create_start_msg(user_name):
    msg = f'Привет, {user_name}!\n\n' \
          f'Мы рады, что ты обратился к нам за помощью! В нашем настолочном боте {"🎲"} ты можешь сдать или взять в аренду ' \
          f'любую настольную игру!\n\n' \
          f'Все очень просто:\n\n' \
          f'1)«Арендовать настолку» - перейти в режим арендатора. {"⌛"} \n\n' \
          f'2)«Сдать настолку» - перейти в режим владельца. {"📦"}\n\n' \
          f'3)«Узнать подробнее о боте» - вывести поробную информацию о боте. {"🧐"} \n\n' \
          f'4)«Вернуться в главное меню» - выйти из текущего режима в главное меню. {"🔙"} \n\n'
    return msg


def create_bot_info_msg():
    msg = f'Арендуйте настольные игры прямо сейчас с помощью нашего чат-бота! \n\n' \
          f'У вас есть желание сыграть в конкретную настолку, но нет возможности ее приобрести?' \
          f'Наш бот предлагает уникальную возможность арендовать настольные игры от владельцев, ' \
          f'которые готовы поделиться своими коллекциями, магазинов и анти-кафе! \n\n' \
          f'• Большой выбор игр от магазинов, анти-кафе и заядлых колллекционеров \n\n' \
          f'• Удобное бронирование и мгновенная аренда \n\n' \
          f'• Безопасность и гарантия целостности игры'
    return msg

def create_delivery_msg():
    msg = f'Доставка осуществляется сторонними сервисами (Достависта, Яндекс Доставка).'
    return msg

def create_payment_msg():
    msg = f'Оплата \n' \
          f'💳 Банковские карты \n\n' \
          f'На данный момент у Вас нет ни одной привязанной карты.' \
          f'Что бы здесь появился список карт, закажите настольную игру или дождитесь, пока арендуют вашу.\n' \
          f'Мы используем встроенный сервис оплаты Телеграмма, поэтому Ваши данные в безопасности.'
    return msg

def create_faq_msg():
    msg = f'У матросов нет вопросов!🙃'
    return msg

def create_first_player_msg():
    msg =   f'Первая аренда! \n\n' \
            f'Настолки – это круто! У нас огромная база, ты обязательно найдешь своё 💞 \n\n' \
            f'Выбери категорию, которая тебе по душе: '
    return msg

def create_random_board_game_msg():
    msg =   f'Рандом \n\n' \
            f'Не знаешь, что выбрать? Брось кубик и положись на удачу 🎲 \n\n'
    return msg

def create_before_check_order_details_msg():
    msg =   f'🏁 Отлично! \n\n' \
            f'Мы почти закончили, осталось только внимательно проверить детали заказа.'
    return msg

def create_check_order_details_msg(order_id, list_of_board_games,
                                   delivery_date, return_date , owner):

    msg =   f"📦 '\033[0m' + Заказ #{order_id} \n" \
            f'📆 С {delivery_date} по {return_date} \n' \
            f'Статус: **в процессе **, \n\n' \
            f"'\033[0m' + Состав \n" \

    for i in range(len(list_of_board_games)):
        msg += f'☑️ {list_of_board_games[i]} \n'


    msg += f'🦄 Владелец {owner}'
    return msg

rent_add_text = "О, Настолочный Владыка!\n" \
                "Пришла пора стереть пыль с коробок 🌚\n\n" \
                "Добавьте свою первую настолку в профиль и назначьте цену 💰"


def getDescGame(json):
    if is_url(json['Rools']):
        return f'📦Название: {json["Status"]} {json["Rating"]}⭐\n\n' \
               f'Краткое описание: \n {json["Description"]}\n\n' \
               f'🕐 {json["Middle_game_time"]} мин\n' \
               f'👥 {json["Min_players"]}-{json["Max_players"]} игроков\n' \
               f'⚠ Возраст +{json["Age"]}\n' \
               f'💡 {json["Category"]} сложность\n\n' \
               f"📜 <a href='{json['Rools']}'>Ссылка на правила</a>\n" \
               f'💰 Цена: {json["Price_per_day"]}/рублей в день'
    else:
        return f'📦Название: {json["Status"]} {json["Rating"]}⭐\n\n' \
               f'Краткое описание: \n {json["Description"]}\n\n' \
               f'🕐 {json["Middle_game_time"]} мин\n' \
               f'👥 {json["Min_players"]}-{json["Max_players"]} игроков\n' \
               f'⚠ Возраст +{json["Age"]}\n' \
               f'💡 {json["Category"]} сложность\n\n' \
               f'💰 Цена: {json["Price_per_day"]}/рублей в день'


def getDescGameFromClass(json):
    return f'📦Название: {json["name"]} {json["rating"]}⭐\n\n' \
           f'Краткое описание: \n {json["desc"]}\n\n' \
           f'🕐 {json["timeGame"]} мин\n' \
           f'👥 {json["minCountPlayers"]}-{json["maxCountPlayers"]} игроков\n' \
           f'⚠ Возраст +{json["age"]}\n' \
           f'💡 {json["category"]} сложность\n\n' \
           f"📜 <a href='{json['rules']}'>Ссылка на правила</a>\n" \
           f'💰 Цена: {json["price"]}/рублей в день'



class BoardGame(StatesGroup):
    name = State()
    desc = State()
    image = State()
    filter = State()
    category = State()
    price = State()
    end = State()

def getDescGameFrom(boardGame):
    return f'📦Название: {boardGame["name"]}\n\n' \
           f'Краткое описание: \n {boardGame["desc"]}\n\n' \
           f'💡 {boardGame["category"]} сложность\n\n' \
           f'💰 Цена: {boardGame["price"]}/рублей в день'


emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)