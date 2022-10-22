import cv2
import numpy as np
import matplotlib.pyplot as plt
import math
import image_getter
import image_handler 
import os

class FilterOverlay():
    
    def __init__(self):
        self.filter_dict = {'sunglasses': 'glasses', 'moustache_hitler': 'moustache',
                            'moustache_stalin': 'moustache', 'trubka_stalin': 'sigarete'}
        self.filter_root = './filters/'
        self.outp_root = './output/'

    def get_image(self, chat_id, filter):
        self.filter = filter
        self.name = chat_id + '.jpg'
        i = image_getter.ImageGetter(self.name)
        self.dict = i.get()
        self.filter_path = self.filter_root + filter + '.png'
        fr = self.filter_dict[filter]
        self.data = image_handler.Filter(self.dict, self.filter_path)
        image = self.data.overlay(fr)
        return image

    def get_path(self, chat_id, filter):
        image = self.get_image(chat_id, filter)
        outp_path = self.outp_root + chat_id + '.jpg'
        plt.imsave(outp_path, image, cmap=plt.cm.hot)
        return outp_path