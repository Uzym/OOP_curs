import random
from dataclasses import dataclass

@dataclass
class Request:
    chat_id: str
    file_url: str # нужно ещё обсудить с ваней что именно ему тут нужно возвращать
    filter_: str

class ProcessingRequests: # сделать так чтобы это был синглтон
    def __init__(self):
        self.request_dict = dict()

    def new_request(self, chat_id, file_url):
        if not(chat_id in self.request_dict.keys()):
            self.request_dict[chat_id] = [file_url, '', 'wait_filter']
        else:
            return False

    def add_filter(self, chat_id, filter):
        if self.request_dict[chat_id][2] == 'wait_filter':
            self.request_dict[chat_id][1] = filter
            self.request_dict[chat_id][2] = 'wait'
        else: # написать нормальные ошибки
            return False

    def get_request(self) -> Request: # тут тоже надо нормальные ошибки
        chat_id, value = '', ['', '', '']
        while value[2] != 'wait': # переписать
            chat_id, value = random.choice(list(self.request_dict.items()))
        self.request_dict[chat_id].append("in_process")
        return Request(chat_id=chat_id, file_url=value[0], filter_=value[1])

    def __str__(self):
        return str(self.request_dict)

requests_queue = ProcessingRequests()
