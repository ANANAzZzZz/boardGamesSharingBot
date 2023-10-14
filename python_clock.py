from datetime import datetime, timedelta
from datetime import time
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from aiogram.types import CallbackQuery


# setting callback_data prefix and parts
#clock_callback = CallbackData('simple_calendar', 'act', 'year', 'month', 'day', 'hour', 'minute')
clock_callback = CallbackData('simple_clock', 'act', 'hour', 'minute')


class SimpleClock:
    async def start_clock(
        self,
        hour: int = datetime.now().hour,
        minute: int = datetime.now().minute
    ) -> InlineKeyboardMarkup:
        """
        Creates an inline keyboard with the provided year and month
        :param int year: Year to use in the calendar, if None the current year is used.
        :param int month: Month to use in the calendar, if None the current month is used.
        :return: Returns InlineKeyboardMarkup object with the calendar.
        """
        
        inline_kb = InlineKeyboardMarkup(row_width=8)
        ignore_callback = clock_callback.new("IGNORE", hour, minute)  # for buttons with no answer

        inline_kb.row()
        inline_kb.insert(InlineKeyboardButton(" Hour ", callback_data=ignore_callback))

        # First row - Month and Year
        inline_kb.row()
        inline_kb.insert(InlineKeyboardButton(
            "<<",
            callback_data=clock_callback.new("PREV-MINUTE", hour, minute)
        ))
        inline_kb.insert(InlineKeyboardButton(
            f'{str(hour)}',
            callback_data=ignore_callback
        ))
        inline_kb.insert(InlineKeyboardButton(
            ">>",
            callback_data=clock_callback.new("NEXT-MINUTE", hour, minute)
        ))


        inline_kb.row()
        inline_kb.insert(InlineKeyboardButton(" Minutes ", callback_data=ignore_callback))

        # Last row - Buttons
        inline_kb.row()
        inline_kb.insert(InlineKeyboardButton(
            "<", callback_data=clock_callback.new("PREV-HOUR", hour, minute)
        ))
        inline_kb.insert(InlineKeyboardButton(f'{str(minute)}', callback_data=ignore_callback))
        inline_kb.insert(InlineKeyboardButton(
            ">", callback_data=clock_callback.new("NEXT-HOUR", hour, minute)
        ))

        # Second row - set time
        inline_kb.row()
        inline_kb.insert(InlineKeyboardButton(" ✔️ ", callback_data=clock_callback.new("CONTINUE", hour, minute)))

        return inline_kb

    async def process_selection(self, query: CallbackQuery, data: CallbackData) -> tuple:
        """
        Process the callback_query. This method generates a new calendar if forward or
        backward is pressed. This method should be called inside a CallbackQueryHandler.
        :param query: callback_query, as provided by the CallbackQueryHandler
        :param data: callback_data, dictionary, set by calendar_callback
        :return: Returns a tuple (Boolean,datetime), indicating if a date is selected
                    and returning the date if so.
        """
        return_data = (False, None)
        temp_date = time(hour = int(data['hour']), minute = int(data['minute']))
        print(temp_date)
        # processing empty buttons, answering with no action
        if data['act'] == "IGNORE":
            await query.answer(cache_time=60)
        if data['act'] == "CONTINUE":
            await query.message.delete_reply_markup()   # removing inline keyboard
            return_data = True, time(hour = int(data['hour']), minute = int(data['minute']))
        # user navigates to previous year, editing message with new calendar
        if data['act'] == "PREV-HOUR":
            prev_date = (datetime(2000, 1, 1, temp_date.hour, temp_date.minute) - timedelta(minutes=15)).time()
            await query.message.edit_reply_markup(await self.start_clock(int(prev_date.hour), int(prev_date.minute)))
        # user navigates to next year, editing message with new calendar
        if data['act'] == "NEXT-HOUR":
            next_date = (datetime(2000, 1, 1, temp_date.hour, temp_date.minute) + timedelta(minutes=15)).time()
            await query.message.edit_reply_markup(await self.start_clock(int(next_date.hour), int(next_date.minute)))
        # user navigates to previous month, editing message with new calendar
        if data['act'] == "PREV-MINUTE":
            prev_date = (datetime(2000, 1, 1, temp_date.hour, temp_date.minute) - timedelta(minutes=60)).time()
            await query.message.edit_reply_markup(await self.start_clock(int(prev_date.hour), int(prev_date.minute)))
        # user navigates to next month, editing message with new calendar
        if data['act'] == "NEXT-MINUTE":
            next_date = (datetime(2000, 1, 1, temp_date.hour, temp_date.minute) + timedelta(minutes=60)).time()
            await query.message.edit_reply_markup(await self.start_clock(int(next_date.hour), int(next_date.minute)))
        # at some point user clicks DAY button, returning date
        return return_data
    


'''
import logging
import datetime
from typing import Dict

from aiogram import Bot, Dispatcher, executor, types
from inline_timepicker.inline_timepicker import InlineTimepicker
from configure import token

API_TOKEN = token

# Configure logging
logging.basicConfig(level=logging.DEBUG)

logging.getLogger('aiogram').setLevel(logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
inline_timepicker = InlineTimepicker()


@dp.message_handler(commands=['time'])
async def send_welcome(message: types.Message):
    inline_timepicker.init(
        datetime.time(12),
        datetime.time(1),
        datetime.time(23),
    )

    await bot.send_message(message.from_user.id,
                           text='test',
                           reply_markup=inline_timepicker.get_keyboard())


@dp.callback_query_handler(inline_timepicker.filter())
async def cb_handler(query: types.CallbackQuery, callback_data: Dict[str, str]):
    await query.answer()
    handle_result = inline_timepicker.handle(query.from_user.id, callback_data)

    if handle_result is not None:
        await bot.edit_message_text(handle_result,
                                    chat_id=query.from_user.id,
                                    message_id=query.message.message_id)
    else:
        await bot.edit_message_reply_markup(chat_id=query.from_user.id,
                                            message_id=query.message.message_id,
                                            reply_markup=inline_timepicker.get_keyboard())


if __name__ == '__main__':
    executor.start_polling(dp)

'''