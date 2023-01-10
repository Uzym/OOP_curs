import os
import uuid
import json
import s3_handler
import processing_requests as pr

import pika
import aio_pika
import asyncio
import logging

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from config import TOKEN, inline_choose_filters, MESSAGES, input_path
from state import BotStates

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())
s3handler = s3_handler.s3Handler()
amqp_url = os.environ["AMQP_URL"]

conn_params = pika.URLParameters(amqp_url)

async def consume():
    
    connection2 = None
    while connection2 == None:
        try:
            connection2 = await aio_pika.connect_robust(amqp_url)
            logging.info('Connected')
        except:
            logging.info('Waiting for connection')
            await asyncio.sleep(50)

    queue_name = "second"
    async with connection2:
        channel2 = await connection2.channel()
        await channel2.set_qos(prefetch_count=10)

        queue = await channel2.declare_queue(queue_name)

        async with queue.iterator() as it:
            async for message in it:
                async with message.process():
                    input = pr.requests_queue.json_deserializer(message.body)
                    print(input)
                    outp_path = input['outp_path']
                    s3handler.download(input['outp_path'])
                    photo = open(outp_path, 'rb')
                    await bot.send_photo(input["chat_id"], photo)
                    await dp.current_state(user=input["chat_id"]).finish()

@dp.message_handler(state='*', commands=['start'])
async def process_start_command(message: types.Message):
    await dp.current_state(user=message.from_user.id).set_state('bot_wait_a_photo')
    await message.reply(MESSAGES['start'])

@dp.message_handler(state=BotStates.BOT_WAIT_A_PHOTO, content_types=['photo'])
async def process_get_image(message: types.Message):
    await dp.current_state(user=message.from_user.id).set_state('bot_wait_a_filter')
    await message.reply(text=MESSAGES['get_image'], reply_markup=inline_choose_filters)
    file_url = message.photo[-1]
    file_info = await bot.get_file(file_url.file_id)
    file_name = str(uuid.uuid4())
    file_path = input_path + file_name + '.' + file_info.file_path.split('photos/')[1].split('.')[-1]
    await file_url.download(file_path)
    s3handler.upload(file_path)
    pr.requests_queue.new_request(message.from_user.id, file_name)
    pr.requests_queue.add_name(message.from_user.id, file_name)
    os.remove(file_path)
    
@dp.callback_query_handler(state=BotStates.BOT_WAIT_A_FILTER)
async def process_callback_filter(callback_query: types.CallbackQuery):
    await dp.current_state(user=callback_query.from_user.id).set_state('bot_wait_a_process')
    await bot.answer_callback_query(callback_query.id)
    pr.requests_queue.add_filter(callback_query.from_user.id, str(callback_query.data))
    await bot.send_message(callback_query.from_user.id, MESSAGES['filter'])
    logging.info(pr.requests_queue.get_request(callback_query.from_user.id))
    req = pr.requests_queue.json_serializer(pr.requests_queue.get_request(callback_query.from_user.id))
    connection = pika.BlockingConnection(conn_params)
    channel = connection.channel()
    channel.queue_declare(queue='first')
    channel.basic_publish(exchange='', routing_key='first', body=req)
    connection.close()

@dp.callback_query_handler(state=BotStates.BOT_WAIT_A_PROCESS)
async def process_callback_wait(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, MESSAGES['filter_wait'])

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(consume())
    executor.start_polling(dp)
