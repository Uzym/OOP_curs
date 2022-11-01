from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from config import TOKEN, inline_choose_filters, MESSAGES
from state import BotStates
import filter_overlay

import processing_requests as pr

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

dp.middleware.setup(LoggingMiddleware())

@dp.message_handler(state='*', commands=['start'])
async def process_start_command(message: types.Message):
    await dp.current_state(user=message.from_user.id).set_state('bot_wait_a_photo')
    await message.reply(MESSAGES['start'])

@dp.message_handler(state='*', commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply(MESSAGES['help'])

@dp.message_handler(state='*', commands=['filters'])
async def process_filters_command(message: types.Message):
    await message.reply(MESSAGES['filters'])

@dp.message_handler(state='*', commands=['list']) # delete
async def process_help_command(message: types.Message):
    await message.reply(str(pr.requests_queue))

@dp.message_handler(state='*', commands=['get']) # delete
async def process_help_command(message: types.Message):
    await message.reply(str(pr.requests_queue.get_request()))

@dp.message_handler(state=BotStates.BOT_WAIT_A_PHOTO, content_types=['photo'])
async def process_get_image(message: types.Message):
    await dp.current_state(user=message.from_user.id).set_state('bot_wait_a_filter')
    await message.reply(text=MESSAGES['get_image'], reply_markup=inline_choose_filters)
    file_url = message.photo[-1]
    pr.requests_queue.new_request(message.from_user.id, file_url)
    file_info = await bot.get_file(file_url.file_id)
    path = './images/'
    file_name = file_info.file_path.split('photos/')[1].split('.')[0]
    pr.requests_queue.add_name(message.from_user.id, file_name)
    await file_url.download(path + file_info.file_path.split('photos/')[1])

@dp.callback_query_handler(state=BotStates.BOT_WAIT_A_FILTER)
async def process_callback_filter(callback_query: types.CallbackQuery):
    await dp.current_state(user=callback_query.from_user.id).set_state('bot_wait_a_process')
    await bot.answer_callback_query(callback_query.id)
    pr.requests_queue.add_filter(callback_query.from_user.id, str(callback_query.data))
    name = pr.requests_queue.get_request()[callback_query.from_user.id][2]
    filter = pr.requests_queue.get_request()[callback_query.from_user.id][1]
    filterOverlay = filter_overlay.FilterOverlay()
    outp_path = filterOverlay.get_path(name, filter)
    photo = open(outp_path, 'rb')
    await bot.send_photo(callback_query.from_user.id, photo)
    #await bot.send_message(callback_query.from_user.id, MESSAGES['filter'])

@dp.callback_query_handler(state=BotStates.BOT_WAIT_A_PROCESS)
async def process_callback_wait(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, MESSAGES['filter_wait'])

@dp.message_handler(state=BotStates.BOT_PROCESS_COMPLETE)
async def process_return_image(callback_query: types.CallbackQuery):
    pass

async def shutdown(dp: Dispatcher):
    await dp.storage.close()
    await dp.storage.wait_closed()

if __name__ == '__main__':
    executor.start_polling(dp)