#!/bin/bash

MMPOSE_FACE_FILE=mmpose/demo/face_img_demo.py
MMPOSE_CONFIG_FILE=mmpose/configs/face/2d_kpt_sview_rgb_img/topdown_heatmap/aflw/hrnetv2_w18_aflw_256x256.py
MMPOSE_CHECKPOINT_FILE=https://download.openmmlab.com/mmpose/face/hrnetv2/hrnetv2_w18_aflw_256x256-f2bbc62b_20210125.pth
IMG_ROOT=mmpose/tests/data/aflw/
IMG=2.jpg
OUTPUT_DIR=mmpose/vis_results

python3 ${MMPOSE_FACE_FILE} \
        ${MMPOSE_CONFIG_FILE} \
        ${MMPOSE_CHECKPOINT_FILE} \
        --img-root ${IMG_ROOT} \
        --img $1 \
        --out-img-root ${OUTPUT_DIR}