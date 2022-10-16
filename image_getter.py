import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2
import subprocess

class ImageGetter():
    
    def __init__(self, image_name):
        self.inp_path = r'./mmpose/tests/data/aflw/'
        self.inp_name = image_name
        self.outp_path = r'./mmpose/vis_results/'
        self.outp_name = self.inp_name.split('.')[0] + '.npy'
        self.script = './mmpose/keypoints_script.sh'
        
    def get(self):
        subprocess.call([self.script, self.inp_name])
        self.keypoints = np.load(self.outp_path + self.outp_name)
        self.image = cv2.imread(self.inp_path + self.inp_name)
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB) 
        return {'image': self.image, 'keypoints': self.keypoints}

    def show(self):
        obj = self.get()
        plt.axis('off')
        plt.imshow(obj['image'])
        plt.scatter(obj['keypoints'][:, 0], obj['keypoints'][:, 1], s=10, c='limegreen')
