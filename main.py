# импортируем библиотеки и наш модуль utils
import random
import utils as ut
from configure import token
from aiogram import Bot, types, Dispatcher, executor

# создаем бота и передаем его диспетчеру(он будет работать с тг)
bot = Bot(token=token)
dp = Dispatcher(bot)

#Хэндлер, реагирующий на текстовое сообщение с текстом “/start”
@dp.message_handler(commands=["start"], is_reply=False)
async def cmd_start(message: types.Message):
    # создаем кнопки
    poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    poll_keyboard.add(types.KeyboardButton(text="Хочу заказать"))
    poll_keyboard.add(types.KeyboardButton(text="Сдаю настолку"))
    poll_keyboard.add(types.KeyboardButton(text="Узнать подробнее о боте"))
    poll_keyboard.add(types.KeyboardButton(text="Вернуться в главное меню"))
    poll_keyboard.add(types.KeyboardButton(text="Попращаться"))
    # выводим начальной сообщение
    hello_sticker = random.choice(ut.hello_stickers)
    start_msg = ut.create_start_msg(message.from_user.first_name)
    await message.answer_sticker(hello_sticker)
    await message.reply(start_msg, reply_markup=poll_keyboard)

#Хэндлер на текстовое сообщение с текстом “Хочу заказат”
@dp.message_handler(lambda message: message.text == "Хочу заказать")
async def action_cancel(message: types.Message):
    await message.reply("Хочу заказать")

#Хэндлер на текстовое сообщение с текстом “Сдаю настолку”
@dp.message_handler(lambda message: message.text == "Сдаю настолку")
async def action_cancel(message: types.Message):
    await message.reply("Сдаю настолку")

#Хэндлер на текстовое сообщение с текстом “Сдаю настолку”
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

#Хэндлер на текстовое сообщение с текстом “Вернуться в главное меню”
@dp.message_handler(lambda message: message.text == "Вернуться в главное меню")
async def action_cancel(message: types.Message):
    await message.reply("Сдаю настолку")

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
    # активируем бота
    executor.start_polling(dp)