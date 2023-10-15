# импортируем библиотеки и наш модуль utils
import json
import random

from aiogram.types import ParseMode
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode
import requests

import urllib.parse
import utils as ut
from configure import token
from aiogram import Bot, types, Dispatcher, executor
from aiogram.types.web_app_info import WebAppInfo
from aiogram_calendar import simple_cal_callback 
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from python_calendar import SimpleCalendar
from python_clock import SimpleClock, clock_callback


# создаем бота и передаем его диспетчеру(он будет работать с тг)
bot = Bot(token=token)
dp = Dispatcher(bot, storage=MemoryStorage())

time_msg = []
board_game_info = None
order_details = {}
delivary_date = 0

def set_main_keyboard_buttons():
    # создаем кнопки
    poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    poll_keyboard.add(types.KeyboardButton(text="Хочу заказать"))
    poll_keyboard.add(types.KeyboardButton(text="Сдаю настолку"))
    poll_keyboard.add(types.KeyboardButton(text="Узнать подробнее о боте"))
    return poll_keyboard

def set_player_keyboard_buttons():
    # создаем кнопки
    kb = [
        [
            types.KeyboardButton(text=f"{'👨‍👩‍👧'} Семейные"), 
            types.KeyboardButton(text=f"{'🎯'} Стратегии")
        ],
        [
            types.KeyboardButton(text=f"{'🧬'} Логические"), 
            types.KeyboardButton(text=f"{'🎉'} Вечериночные")
        ],
        [
            types.KeyboardButton(text=f"{'🥂'} Кооперативные"),
            types.KeyboardButton(text=f"{'❓'} Не могу определиться")
        ],
    ]
    poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=kb)
    return poll_keyboard

def set_board_games_buttons():
    # создаем кнопки
    board_games_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    board_games_keyboard.add(types.KeyboardButton(text='Просмотреть список', web_app=WebAppInfo(
        url="https://hack1.alieksandrzviez.repl.co/")))
    board_games_keyboard.add(types.KeyboardButton(text="Вернуться в главное меню"))
    return board_games_keyboard

def check_order_board_game_status(game_status):
    if isinstance(game_status, int):
        return "Завершен" if not game_status else "В процессе"
    return game_status

#############################################

#Хэндлер, реагирующий на текстовое сообщение с текстом “/start”
@dp.message_handler(commands=["start"], is_reply=False)
async def cmd_start(message: types.Message):
    # выводим начальной сообщение
    hello_sticker = random.choice(ut.hello_stickers)
    start_msg = ut.create_start_msg(message.from_user.first_name)
    buttons = set_main_keyboard_buttons()
    await message.answer_sticker(hello_sticker)
    await message.reply(start_msg, reply_markup=buttons)

#############################################

#Хэндлер на текстовое сообщение с текстом “Хочу заказать”
@dp.message_handler(lambda message: message.text == "Хочу заказать")
async def cmd_player_board_game(message: types.Message):
    first_player_msg = ut.create_first_player_msg()
    buttons = set_player_keyboard_buttons()
    await message.reply(first_player_msg, reply_markup=buttons)

#Хэндлер на текстовое сообщение с текстом “Кооперативные”
@dp.message_handler(lambda message: message.text == f"{'👨‍👩‍👧'} Семейные")
async def cmd_choose_party_board_game(message: types.Message):
    buttons = set_board_games_buttons()
    await message.answer("Открыть список настолок: ", reply_markup = buttons)

#Хэндлер на текстовое сообщение с текстом “Кооперативные”
@dp.message_handler(lambda message: message.text == f"{'🎯'} Стратегии")
async def cmd_choose_party_board_game(message: types.Message):
    buttons = set_board_games_buttons()
    await message.answer("Открыть список настолок: ", reply_markup = buttons)

#Хэндлер на текстовое сообщение с текстом “Кооперативные”
@dp.message_handler(lambda message: message.text == f"{'🧬'} Логические")
async def cmd_choose_party_board_game(message: types.Message):
    buttons = set_board_games_buttons()
    await message.answer("Открыть список настолок: ", reply_markup = buttons)

#Хэндлер на текстовое сообщение с текстом “Кооперативные”
@dp.message_handler(lambda message: message.text == f"{'🎉'} Вечериночные")
async def cmd_choose_party_board_game(message: types.Message):
    buttons = set_board_games_buttons()
    await message.answer("Открыть список настолок: ", reply_markup = buttons)

#Хэндлер на текстовое сообщение с текстом “Кооперативные”
@dp.message_handler(lambda message: message.text == f"{'🥂'} Кооперативные")
async def cmd_choose_cooperative_board_game(message: types.Message):
    buttons = set_board_games_buttons()
    await message.answer("Выберите действие: ", reply_markup = buttons)

@dp.message_handler(content_types=['web_app_data'])
async def get_player_board_game_message(message: types.Message):
    board_game = json.loads(message.web_app_data.data)
    
    try:
        global board_game_info
        board_game_info = board_game
        flag = board_game["artyom"]
        print(flag)
        try:
            kb = [
                [
                    types.InlineKeyboardButton(text=f"{'💎'} Арендовать", callback_data='zodiac')
                ],
                [
                    types.InlineKeyboardButton(text=f"⏪‍", callback_data='zodiac'),
                    types.InlineKeyboardButton(text=f"⏩", callback_data='zodiac')
                ]
            ]
            rent_keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
            await message.answer_photo(caption=ut.getDescGame(board_game),
                                    photo=urllib.parse.urlparse(board_game["Image"]).geturl(), parse_mode=ParseMode.HTML,
                                    reply_markup=rent_keyboard)
        except:
            await ut.BoardGame.name.set()
            await message.answer("Укажите дату доставки: ", reply_markup= await SimpleCalendar().start_calendar())
    except:
        try:
            kb = [
                [
                    types.InlineKeyboardButton(text=f"{'💎'} Арендовать", callback_data='zodiac')
                ],
                [
                    types.InlineKeyboardButton(text=f"⏪‍", callback_data='zodiac'),
                    types.InlineKeyboardButton(text=f"⏩", callback_data='zodiac')
                ]
            ]
            rent_keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
            await message.answer_photo(caption=ut.getDescGame(board_game),
                                    photo=urllib.parse.urlparse(board_game["img"]).geturl(), parse_mode=ParseMode.HTML,
                                    reply_markup=rent_keyboard)
        except:
            await ut.BoardGame.name.set()
            await message.answer(text='🔥ВАУ Редкая настолка!\n'
                                    'Давай расскажем о ней миру\n\n'
                                    '**1/6** Как она назвается?')

# simple calendar usage
@dp.callback_query_handler(simple_cal_callback.filter())
async def process_simple_calendar(callback_query: types.CallbackQuery, callback_data: dict):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        await callback_query.message.answer(f'Дата: {date.strftime("%d/%m/%Y")}')
        time_msg.append(f'{date.strftime("%d/%m/%Y")}')
        await callback_query.message.answer("Укажите время: ", reply_markup=await SimpleClock().start_clock())
        
# simple clock usage
@dp.callback_query_handler(clock_callback.filter())
async def process_simple_clock(callback_query: types.CallbackQuery, callback_data: dict):
    global delivary_date
    selected, date = await SimpleClock().process_selection(callback_query, callback_data)
    if selected:
        await callback_query.message.answer(f'Время: {date.strftime("%H:%M")}')
        time_msg.append(f'{date.strftime("%H:%M")}')
        delivary_date +=1
        if delivary_date > 1:
            poll_keyboard = types.InlineKeyboardMarkup()
            poll_keyboard.add(types.InlineKeyboardButton(text = f"{'✅'} Оформить заказ", callback_data='place_order'))
            await callback_query.message.answer(ut.create_before_check_order_details_msg(), reply_markup = poll_keyboard)
        else:
            await callback_query.message.answer("Укажите дату и время сдачи: ", reply_markup=await SimpleCalendar().start_calendar())

@dp.callback_query_handler(lambda c: c.data == 'place_order')
async def check_order_details(callback_query: types.CallbackQuery):
    global time_msg, board_game_info

    print(board_game_info)

    board_game_msg = {"delivery_date": time_msg[0], "return_date": time_msg[2],
                      "ID_Boardgame":board_game_info["ID_Boardgame"],"ID_Owner":board_game_info["ID_Owner"],
                      "ID_Renter":board_game_info["ID_Renter"]}
    
    await bot.send_photo(callback_query.from_user.id, "https://m.media-amazon.com/images/I/813J0DBqCTL._AC_UF894,1000_QL80_.jpg",
                        caption=ut.create_check_order_details_msg(board_game_info["ID"], [board_game_info["Status"]], 
                        time_msg[0], time_msg[2], callback_query.from_user.full_name),
                        reply_markup=types.ReplyKeyboardRemove())
    
    response = requests.get(
                f"https://humorous-ringtail-abnormally.ngrok-free.app/addOrder?Order_time={board_game_msg['delivery_date']}"
                f"&ID_renter={board_game_msg['ID_Renter']}&ID_boardgame={board_game_msg['ID_Boardgame']}&ID_owner={board_game_msg['ID_Owner']}"
            )
    
    print(response.status_code)
    
    await callback_query.message.reply(ut.create_start_msg(callback_query.from_user.first_name), reply_markup=set_main_keyboard_buttons())

#Хэндлер на текстовое сообщение с текстом “Не могу определиться”
@dp.message_handler(lambda message: message.text == f"{'❓'} Не могу определиться")
async def cmd_unknown_board_game(message: types.Message):
    random_board_game_msg = ut.create_random_board_game_msg()
    poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    poll_keyboard.add(types.KeyboardButton(text=f"{'🔮'} Рандомная игра"))
    poll_keyboard.add(types.KeyboardButton(text="Вернуться в главное меню"))
    await message.reply(random_board_game_msg, reply_markup=poll_keyboard)

#Хэндлер на текстовое сообщение с текстом “{'🔮'} Рандомная игра"”
@dp.message_handler(lambda message: message.text == f"{'🔮'} Рандомная игра")
async def cmd_get_random_board_game(message: types.Message):
    poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    poll_keyboard.add(types.KeyboardButton(text="Вернуться в главное меню"))
    await message.reply("Скоро появится...", reply_markup=poll_keyboard)

#############################################

# Хэндлер на текстовое сообщение с текстом “Сдаю настолку”
@dp.message_handler(lambda message: message.text == "Сдаю настолку")
async def cmd_rent_board_game(message: types.Message):
    await message.answer(ut.rent_add_text)
    rent_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    rent_keyboard.add(types.KeyboardButton(text='Добавить настолку', web_app=WebAppInfo(
        url="https://hack.alieksandrzviez.repl.co")))
    rent_keyboard.add(types.KeyboardButton(text="Вернуться в главное меню"))
    # отправляем вспомогательное сообщение
    await message.answer('Выберите действие:', reply_markup=rent_keyboard)

# 1/6 set name
@dp.message_handler(state=ut.BoardGame.name)
async def insert_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    await ut.BoardGame.next()
    await message.answer("**2/6** Теперь описание.\nМожешь совсем кратенько, если что мы дополним 😼")


# 2/6 set desc
@dp.message_handler(state=ut.BoardGame.desc)
async def insert_desc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['desc'] = message.text

    await ut.BoardGame.next()
    await message.answer("**3/6** Укажи ссылку на картинку, чтобы привлечь внимание")


# 3/6 set image
@dp.message_handler(state=ut.BoardGame.image)
async def insert_image(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['image'] = message.text

    await ut.BoardGame.next()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("👨‍👩‍👧 семейные", "🎯стратегии")
    markup.add("🧬 логические", "🎉 вечериночные")
    markup.add("🥂 кооперативные")

    await message.answer("**4/6** К какой категории отнесешь ее?", reply_markup=markup)


# 4/6 set filter
@dp.message_handler(state=ut.BoardGame.filter)
async def insert_filter(message: types.Message, state: FSMContext):
    await ut.BoardGame.next()
    await state.update_data(filter=ut.emoji_pattern.sub(r'', message.text).strip())

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("💅 Легкая", "😅 Средняя")
    markup.add("🙀 Сложная", "💀 Нереальная")

    await message.answer("**5/6** Насколько сложная настольная игра?", reply_markup=markup)


# 5/6 set category
@dp.message_handler(state=ut.BoardGame.category)
async def insert_desc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['category'] = ut.emoji_pattern.sub(r'', message.text).strip()

    await ut.BoardGame.next()
    await message.answer("**6/6** И самое приятное...\nНазначь цену за сутки", reply_markup=types.ReplyKeyboardRemove())


# Сохраняем пол, выводим анкету
@dp.message_handler(state=ut.BoardGame.price)
async def process_gender(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text

    kb = [
        [
            types.InlineKeyboardButton(text=f"{'↩'} Изменить", callback_data='zodiac'),
            types.InlineKeyboardButton(text=f"❌ Отменить", callback_data='zodiac')
        ],
        [

            types.InlineKeyboardButton(text=f"🚀 Опубликовать", callback_data='zodiac')
        ]
    ]
    rent_keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)

    data = await state.get_data()
    await message.answer_photo(caption=ut.getDescGameFrom(data),
                               photo=urllib.parse.urlparse(data["image"]).geturl(), parse_mode=ParseMode.HTML,
                               reply_markup=rent_keyboard)

    await state.finish()

#############################################

#Хэндлер на текстовое сообщение с текстом “Узнать подробнее о боте”
@dp.message_handler(lambda message: message.text == "Узнать подробнее о боте")
async def cmd_bot_info(message: types.Message):
    # создаем кнопки
    poll_keyboard = types.InlineKeyboardMarkup()
    poll_keyboard.add(types.InlineKeyboardButton(text=f"{'🚴'} Доставка", callback_data='delivery'))
    poll_keyboard.add(types.InlineKeyboardButton(text=f"{'💰'} Оплата", callback_data='payment'))
    poll_keyboard.add(types.InlineKeyboardButton(text=f"{'❓'} FAQ", callback_data='faq'))
    # выводим начальной сообщение
    start_msg = ut.create_bot_info_msg()
    await message.reply(start_msg, reply_markup=poll_keyboard)

#Хэндлер на нажатие кнопки “Доставка”
@dp.callback_query_handler(lambda c: c.data == 'delivery')
async def process_delivery_button(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, ut.create_delivery_msg())

#Хэндлер на нажатие кнопки “Доставка”
@dp.callback_query_handler(lambda c: c.data == 'payment')
async def process_payment_button(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, ut.create_payment_msg())

#Хэндлер на нажатие кнопки “Доставка”
@dp.callback_query_handler(lambda c: c.data == 'faq')
async def process_faq_button(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, ut.create_faq_msg())

#############################################

#Хэндлер на текстовое сообщение с текстом “Вернуться в главное меню”
@dp.message_handler(lambda message: message.text == "Вернуться в главное меню")
async def cmd_return_main_menu(message: types.Message):
    buttons = set_main_keyboard_buttons()
    await message.reply(ut.create_start_msg(message.from_user.first_name), reply_markup=buttons)


# условие проходит, если мы запускаем именно этот скрипт, а тк
# это главный исполняющий файл, то условие всегда true
if __name__ == '__main__':

    dp.register_callback_query_handler(process_simple_clock,simple_cal_callback.filter())
    # активируем бота
    executor.start_polling(dp)
