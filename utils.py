# импортируем библиотеки

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
    msg =   f'Привет, {user_name}!\n\n' \
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
    msg =   f'Арендуйте настольные игры прямо сейчас с помощью нашего чат-бота! \n\n' \
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

def create_delivery_msg():
    msg = f'Курьер из Яндекс.Еда'
    return msg

def create_payment_msg():
    msg = f'Оплата возможна с помощью карты'
    return msg

def create_faq_msg():
    msg = f'1. Это безопасно? (Нет)'
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

rent_add_text = "О, Настолочный Владыка!\n" \
                "Пришла пора стереть пыль с коробок 🌚\n\n" \
                "Добавьте свою первую настолку в профиль и назначьте цену 💰"
