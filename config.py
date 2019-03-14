#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2019/3/13 10:40
# @Author  : wendy
# @Usage   : Set some global config here
# @File    : config.py
# @Software: PyCharm
import cv2

COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
FONT = cv2.FONT_HERSHEY_SIMPLEX
# using author's best trained model as default
SINGLE_NET_NAME = 'ssd_300_VOC0712.pth'
NET_POSITION = './checkpoints'
DEFAULT_VIDEO_SOURCE = 'video_file' # change to `camera` if you like
ICON_PATH = 'ui/zebraCross.ico'

DEFAULT_RESULT_PATH = 'my_dataset/result'
MAX_SAVED_IMAGE = 10
PREDICT_RESULT_PATH = 'predict_text/'
PREDICT_RESULT_IMAGE = 'predict_image/'

