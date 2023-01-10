import random
from dataclasses import dataclass
import json
import os
import pika

file_path = './'

@dataclass
class Request:
    chat_id: str
    file_url: str
    filter_: str

class ProcessingRequests:
    def __init__(self):
        self.request_dict = dict()
        self.amqp_url = os.environ["AMQP_URL"]

    @staticmethod
    def json_deserializer(m):
        return json.loads(m.decode('utf-8'))

    @staticmethod
    def json_serializer(data):
        return json.dumps(data).encode("utf-8")

    def new_request(self, chat_id, name):
        if not(chat_id in self.request_dict.keys()):
            self.request_dict[chat_id] = {'chat_id': chat_id, 'filter': '', 'name': name}
        else:
            return False

    def add_name(self, chat_id, name):
        self.request_dict[chat_id]['name'] = name

    def add_filter(self, chat_id, filter):
        self.request_dict[chat_id]['filter'] = filter

    def get_request(self, chat_id) -> Request:
        return self.request_dict[chat_id]

    def __str__(self):
        return str(self.request_dict)

requests_queue = ProcessingRequests()
