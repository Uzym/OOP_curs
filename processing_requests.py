import random
from dataclasses import dataclass

file_path = './'

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
            self.request_dict[chat_id] = [file_url, '', '']
        else:
            return False

    def add_filter(self, chat_id, filter):
        self.request_dict[chat_id][1] = filter

    def add_name(self, chat_id, name):
        self.request_dict[chat_id][2] = name

    def get_request(self) -> Request:
        return self.request_dict

    def __str__(self):
        return str(self.request_dict)

requests_queue = ProcessingRequests()