# импортируем библиотеки и наш модуль utils
import random
import utils as ut
from configure import token
from aiogram import Bot, types, Dispatcher, executor

# создаем бота и передаем его диспетчеру(он будет работать с тг)
bot = Bot(token=token)
dp = Dispatcher(bot)

# коды смайликов, нужны для распечатки в сообщениях
smile1 = '\U0001F4F0'
smile2 = '\U0001F4E2'
smile3 = '\U0001F4CC'
smile4 = '\U0001F393'
smile5 = '\U0001F6A9'
smile6 = '\U0001F601'


# Хэндлер, реагирующий на текстовое сообщение с текстом “/start”
@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    # создаем кнопки
    poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    poll_keyboard.add(types.KeyboardButton(text='Привет!'))
    poll_keyboard.add(types.KeyboardButton(text="Хочу заказать"))
    poll_keyboard.add(types.KeyboardButton(text="Сдаю настолку"))
    poll_keyboard.add(types.KeyboardButton(text="Пока!"))
    # отправляем вспомогательное сообщение
    await message.reply('Выберите действие:', reply_markup=poll_keyboard)


# Хэндлер на текстовое сообщение с текстом “Привет!”
@dp.message_handler(lambda message: message.text == "Привет!")
async def action_cancel(message: types.Message):
    # выбираем случайный стикер(из нашего множества) для приветствия
    el = random.choice(ut.stikers_id1)
    # узнаем имя пользователя
    name = message.from_user.first_name
    # отправляем стикер
    await message.answer_sticker(el)
    # отправляем сообщение
    await message.reply(
        f"Привет, {name}! Я твой личный мобильный помощник, буду помогать тебе во время обучения в ГУАП!\n\n"
        "Что я умею?\n\n"
        f"   1)Покажу все мероприятия, которые сейчас проходят в вузе или будут проводиться. {smile4}\n\n"
        f"   2)Расскажу обо всех важных объявлениях, чтобы ты оставался в курсе последних событий. {smile5}\n\n"
        f"   3)Напомню расписание твоей группы, а то вдруг ты его забыл). {smile6}")


# Хэндлер на текстовое сообщение с текстом “Хочу заказать”
@dp.message_handler(lambda message: message.text == "Хочу заказать")
async def action_cancel(message: types.Message):
    await message.reply("Хочу заказать")


# Хэндлер на текстовое сообщение с текстом “Сдаю настолку”
@dp.message_handler(lambda message: message.text == "Сдаю настолку")
async def action_cancel(message: types.Message):
    await message.answer(ut.rent_add_text)
    rent_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    rent_keyboard.add(types.KeyboardButton(text='Добавить настолку'))
    # отправляем вспомогательное сообщение
    await message.answer('Выберите действие:', reply_markup=rent_keyboard)


# Хэндлер на текстовое сообщение с текстом “Пока!”
@dp.message_handler(lambda message: message.text == "Пока!")
async def action_cancel(message: types.Message):
    # берем случайных стикер для прощания
    el = random.choice(ut.stikers_id2)
    # узнаем имя пользователя
    name = message.from_user.first_name
    # отправляем сообщение
    await message.reply(f"Всего хорошего, {name}! Заглядывай почаще!")
    # отправляем стикер
    await message.answer_sticker(el)
    # убираем клавиатуру
    remove_keyboard = types.ReplyKeyboardRemove()
    # выводи вспомогательное сообщение
    await message.answer("Введите /start, чтобы начать заново.", reply_markup=remove_keyboard)


# условие проходит, если мы запускаем именно этот скрипт, а тк
# это главный исполняющий файл, то условие всегда true
if __name__ == '__main__':
    # активируем бота
    executor.start_polling(dp)
