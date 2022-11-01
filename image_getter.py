import os
import warnings
import numpy as np
import cv2
import matplotlib.pyplot as plt
from mmpose.apis import (inference_top_down_pose_model, init_pose_model,
                         vis_pose_result)
from mmpose.datasets import DatasetInfo

try:
    import face_recognition
    has_face_det = True
except (ImportError, ModuleNotFoundError):
    has_face_det = False


class ImageGetter():
    
    def __init__(self):
        pose_config_file = "./mmpose/configs/face/2d_kpt_sview_rgb_img/topdown_heatmap/aflw/hrnetv2_w18_aflw_256x256.py"
        pose_checkpoint_file = "./mmpose/input/hrnetv2_w18_aflw_256x256-f2bbc62b_20210125.pth"
        self.img_root = "./images/"
        self.pose_model = init_pose_model(pose_config_file, pose_checkpoint_file, device='cuda:0')

    def process_face_det_results(self, face_det_results):
        person_results = []
        for bbox in face_det_results:
            person = {}
            # left, top, right, bottom
            person['bbox'] = [bbox[3], bbox[0], bbox[1], bbox[2]]
            person_results.append(person)

        return person_results

    def get(self, img_name):
        dataset = self.pose_model.cfg.data['test']['type']
        dataset_info = self.pose_model.cfg.data['test'].get('dataset_info', None)
        if dataset_info is None:
            warnings.warn(
                'Please set `dataset_info` in the config.'
                'Check https://github.com/open-mmlab/mmpose/pull/663 for details.',
                DeprecationWarning)
        else:
            dataset_info = DatasetInfo(dataset_info)
        
        image_name = os.path.join(self.img_root, img_name)
        image = face_recognition.load_image_file(image_name)
        face_det_results = face_recognition.face_locations(image)
        face_results = self.process_face_det_results(face_det_results)
        return_heatmap = False
        output_layer_names = None

        pose_results, returned_outputs = inference_top_down_pose_model(
                self.pose_model,
                image_name,
                face_results,
                bbox_thr=None,
                format='xyxy',
                dataset=dataset,
                dataset_info=dataset_info,
                return_heatmap=return_heatmap,
                outputs=output_layer_names)
        
        return {'image': image, 'keypoints': pose_results[0]['keypoints']}

    def show(self, img_name):
        obj = self.get(img_name)
        plt.axis('off')
        plt.imshow(obj['image'])
        plt.scatter(obj['keypoints'][:, 0], obj['keypoints'][:, 1], s=10, c='limegreen')