FROM python:3.10.6
COPY *.txt ./
COPY *.py ./
COPY *.pth ./
ADD ./archive.tar.xz ./
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip3 install cmake
RUN pip3 install dlib
RUN pip3 install face_recognition
RUN pip3 install -U -r requirements.txt

ARG PYTORCH="1.6.0"
ARG CUDA="10.1"
ARG CUDNN="7"
ARG MMCV="1.7.0"

# To fix GPG key error when running apt-get update
RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/3bf863cc.pub
RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1804/x86_64/7fa2af80.pub

RUN apt-get update && apt-get install -y git ninja-build libglib2.0-0 libsm6 libxrender-dev libxext6 libgl1-mesa-glx\
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install xtcocotools
RUN pip install cython
RUN pip install xtcocotools
RUN pip install -U openmim
RUN mim install mmcv==${MMCV}
# Install MMCV

ENTRYPOINT [ "python3", "server.py" ]
