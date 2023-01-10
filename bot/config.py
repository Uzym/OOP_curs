from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "5468492351:AAFwz4kDSSXhGDWIxcfOssOGDtf1Nda2wCQ"

input_path = './input/'
output_path = './output/'
filter_list = [('Черные очки', 'sunglasses', 'Просто крутые черные очки че тут ещё говорить?'),               
               ('Усы Гитлера', 'moustache_hitler', 'Неодобряем ваши интересы'),
               ('Усы Сталина', 'moustache_stalin', 'Одобряем ваши интересы'),               
               ('Трубка Сталина', 'trubka_stalin', 'Просто мегакрутая трубка ТОВАРИЩА СТАЛИНА')]

inline_choose_filters = InlineKeyboardMarkup()
for filter_item in filter_list:
    inline_choose_filters.add(InlineKeyboardButton(text=filter_item[0], callback_data=filter_item[1]))

help_message = "Данный бот может наложить простые фильтры на лицо человека.\n" \
               "/help справка\n" \
               "/filters списко доступных фильтров\n" \
               "/start запуск бота" \

filter_list_message = "Доступные фильтры\n" + \
                      ''.join([filter_item[0] + ": " + filter_item[2] + '\n' for filter_item in filter_list])

start_message = "Отправте мне фотографию с вашим лицом!"
callback_filter_message = "Ваша фотография в очереди. Ожидайте"
callback_filter_wait_message = "Подождите пока обработается ваш запрос"
MESSAGES = {
    'start': start_message,    
    'help': help_message,    
    'filters': filter_list_message,    
    'filter': callback_filter_message,    
    'filter_wait': callback_filter_wait_message,    
    'get_image': "Доступные фильтры:"}