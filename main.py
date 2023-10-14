# импортируем библиотеки и наш модуль utils
import random
import utils as ut
from configure import token
from aiogram import Bot, types, Dispatcher, executor
from aiogram.types.web_app_info import WebAppInfo
from aiogram_calendar import simple_cal_callback 
from python_calendar import SimpleCalendar
from python_clock import SimpleClock, clock_callback
from inline_timepicker.inline_timepicker import InlineTimepicker


# создаем бота и передаем его диспетчеру(он будет работать с тг)
bot = Bot(token=token)
dp = Dispatcher(bot)
inline_timepicker = InlineTimepicker()


def set_main_keyboard_buttons():
    # создаем кнопки
    poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    poll_keyboard.add(types.KeyboardButton(text="Хочу заказать"))
    poll_keyboard.add(types.KeyboardButton(text="Сдаю настолку"))
    poll_keyboard.add(types.KeyboardButton(text="Узнать подробнее о боте"))
    poll_keyboard.add(types.KeyboardButton(text="Вернуться в главное меню"))
    poll_keyboard.add(types.KeyboardButton(text="Попращаться"))
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
    await message.answer("Please select a date: ", reply_markup=await SimpleCalendar().start_calendar())

#Хэндлер на текстовое сообщение с текстом “Кооперативные”
@dp.message_handler(lambda message: message.text == f"{'🎯'} Стратегии")
async def cmd_choose_party_board_game(message: types.Message):
    await message.answer("Please select a date: ", reply_markup=await SimpleCalendar().start_calendar())

#Хэндлер на текстовое сообщение с текстом “Кооперативные”
@dp.message_handler(lambda message: message.text == f"{'🧬'} Логические")
async def cmd_choose_party_board_game(message: types.Message):
    await message.answer("Please select a date: ", reply_markup=await SimpleCalendar().start_calendar())

#Хэндлер на текстовое сообщение с текстом “Кооперативные”
@dp.message_handler(lambda message: message.text == f"{'🎉'} Вечериночные")
async def cmd_choose_party_board_game(message: types.Message):
    await message.answer("Please select a date: ", reply_markup=await SimpleCalendar().start_calendar())

#Хэндлер на текстовое сообщение с текстом “Кооперативные”
@dp.message_handler(lambda message: message.text == f"{'🥂'} Кооперативные")
async def cmd_choose_cooperative_board_game(message: types.Message):
    await message.answer("Please select a date: ", reply_markup=await SimpleCalendar().start_calendar())

# simple calendar usage
@dp.callback_query_handler(simple_cal_callback.filter())
async def process_simple_calendar(callback_query: types.CallbackQuery, callback_data: dict):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        await callback_query.message.answer(
            f'You selected {date.strftime("%d/%m/%Y")}',
        )
        await callback_query.message.answer("Please select time: ", reply_markup=await SimpleClock().start_clock())
        
# simple clock usage
@dp.callback_query_handler(clock_callback.filter())
async def process_simple_clock(callback_query: types.CallbackQuery, callback_data: dict):
    selected, date = await SimpleClock().process_selection(callback_query, callback_data)
    if selected:
        await callback_query.message.answer(
            f'You selected {date.strftime("%H:%M")}',
        )

#Хэндлер на текстовое сообщение с текстом “Не могу определиться”
@dp.message_handler(lambda message: message.text == f"{'❓'} Не могу определиться")
async def cmd_get_random_board_game(message: types.Message):
    random_board_game_msg = ut.create_random_board_game_msg()
    poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    poll_keyboard.add(types.KeyboardButton(text="{'🔮'} Рандомная игра"))
    await message.reply(random_board_game_msg, reply_markup=poll_keyboard)

#############################################

# Хэндлер на текстовое сообщение с текстом “Сдаю настолку”
@dp.message_handler(lambda message: message.text == "Сдаю настолку")
async def cmd_rent_board_game(message: types.Message):
    await message.answer(ut.rent_add_text)
    rent_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    rent_keyboard.add(types.KeyboardButton(text='Открыть веб-страницу', web_app=WebAppInfo(
        url="https://hack.alieksandrzviez.repl.co")))
    # отправляем вспомогательное сообщение
    await message.answer('Выберите действие:', reply_markup=rent_keyboard)

#############################################

#Хэндлер на текстовое сообщение с текстом “Узнать подробнее о боте”
@dp.message_handler(lambda message: message.text == "Узнать подробнее о боте")
async def cmd_bot_info(message: types.Message):
    # создаем кнопки
    poll_keyboard = types.InlineKeyboardMarkup()
    poll_keyboard.add(types.InlineKeyboardButton(text = f"{'🚴'} Доставка", callback_data='delivery'))
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
    await message.reply(" 1 ", reply_markup=buttons)

#############################################

#Хэндлер на текстовое сообщение с текстом “Пока!”
@dp.message_handler(lambda message: message.text == "Пока!")
async def cmd_end(message: types.Message):
    # убираем клавиатуру
    remove_keyboard = types.ReplyKeyboardRemove()
    # выводим конечное сообщение
    bye_sticker = random.choice(ut.bye_stickers)
    end_msg = ut.create_end_msg(message.from_user.first_name)
    await message.answer_sticker(bye_sticker)
    await message.reply(end_msg)
    # выводи вспомогательное сообщение
    await message.answer("Введите /start, чтобы начать заново.", reply_markup=remove_keyboard)


# условие проходит, если мы запускаем именно этот скрипт, а тк
# это главный исполняющий файл, то условие всегда true
if __name__ == '__main__':

    dp.register_callback_query_handler(process_simple_clock,simple_cal_callback.filter())
    # активируем бота
    executor.start_polling(dp)
