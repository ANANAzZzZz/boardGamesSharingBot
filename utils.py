# импортируем библиотеки
import aiogram
from aiogram.dispatcher.filters import Text
from yarl import URL

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
          f'1)"Арендовать настолку" - перейти в режим арендатора. {"⌛"} \n\n' \
          f'2)"Сдать настолку" - перейти в режим владельца. {"📦"}\n\n' \
          f'3)"Узнать подробнее о боте" - вывести поробную информацию о боте. {"🧐"} \n\n' \
          f'4)"Вернуться в главное меню" - выйти из текущего режима в главное меню. {"🔙"} \n\n' \
          f'5)"Попращаться" - попращаться с ботом. {"👋"}'
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


def create_end_msg(user_name):
    msg = f'Всего хорошего, {user_name}! Заглядывай почаще!'
    return msg


rent_add_text = "О, Настолочный Владыка!\n" \
                "Пришла пора стереть пыль с коробок 🌚\n\n" \
                "Добавьте свою первую настолку в профиль и назначьте цену 💰"


def getDescGame(json):
    return f'📦Название: {json["name"]} {json["world_rating"]}⭐\n\n' \
           f'Краткое описание: \n {json["desc"]}\n\n' \
           f'🕐 {json["middle_game_time"]} мин\n' \
           f'👥 {json["min_players"]}-{json["max_players"]} игроков\n' \
           f'⚠ Возраст +{json["age"]}\n' \
           f'💡 {json["category"]} сложность\n\n' \
           f"📜 <a href='{json['rools']}'>Ссылка на правила</a>\n" \
           f'💰 Цена: {json["price_day"]}/рублей в день'
