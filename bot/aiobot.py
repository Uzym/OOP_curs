from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import processing_requests as pr

TOKEN = "5286234589:AAFlkQObco_9UBbyFplKJjJxe6Ojiri6dEQ"

filter_list = [InlineKeyboardButton(text='Черные очки', callback_data='sun_glasses'),
               InlineKeyboardButton(text='Сигарета', callback_data='siga'),
               InlineKeyboardButton(text='Ещё какое то говно', callback_data='shit')]
inline_choose_filters = InlineKeyboardMarkup()
for filter_item in filter_list:
    inline_choose_filters.add(filter_item)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!\nОтправте мне фотографию с вашим лицом!")

@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Данный бот может наложить простые фильтры на лицо человека. "
                        "Просто отправте фотографию и выберите фильтр.")

@dp.message_handler(commands=['list'])
async def process_help_command(message: types.Message):
    await message.reply(str(pr.requests_queue))

@dp.message_handler(content_types=['photo'])
async def process_get_image(message: types.Message):
    await message.reply("Доступные фильтры:", reply_markup=inline_choose_filters)
    file_url = message.photo[0]
    pr.requests_queue.new_request(message.from_user.id, file_url)

@dp.callback_query_handler()
async def process_callback_filter(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    #await bot.send_message(callback_query.from_user.id, str(callback_query.data))
    pr.requests_queue.add_filter(callback_query.from_user.id, str(callback_query.data))

if __name__ == '__main__':
    executor.start_polling(dp)
