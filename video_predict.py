#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2019/3/10 14:59
# @Author  : wendy
# @Usage   : The predictions of video mode
# @File    : video_predict.py
# @Software: PyCharm
import os
from time import sleep
import torch
import cv2
from torch.autograd import Variable
from data import BaseTransform, VOC_CLASSES as labelmap
from ssd import build_ssd

COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
FONT = cv2.FONT_HERSHEY_SIMPLEX
# using author's best trained model as default
SINGLE_NET_NAME = 'ssd300_mAP_77.43_v2.pth'
# NET_POSITION = './checkpoints'
MAX_SAVED_IMAGE = 20

def get_predicts(net,transform,saveDir='my_dataset/video_frame'):

    if not os.path.exists(saveDir):
        os.makedirs(saveDir)
    count = 1  # 图片计数索引
    cap = cv2.VideoCapture(0)
    width, height = 1280, 480
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    print ('width: ', width)
    print ('height: ', height)

    while True:

        if key == 27 or count == MAX_SAVED_IMAGE:  # exit
            break

        ret, frame = cap.read()  # 获取相框
        frame = cv2.flip(frame, 1, dst=None)  #此处使用flip进行水平镜像处理
        frame = frame_predict(net,frame,transform)

        cv2.imshow("video_detect", frame)
        key = cv2.waitKey(1) & 0xFF
        print('awaking and saving pic...')
        cv2.imwrite("%s/%d.jpg" % (saveDir, count), cv2.resize(frame, (300, 300), interpolation=cv2.INTER_AREA))
        print(u"%s: %d 张图片" % (saveDir, count))
        count += 1
        sleep(5)

    cap.release()  # 释放摄像头
    cv2.destroyAllWindows()  # 丢弃窗口

def frame_predict(net,frame,transform):

    height, width = frame.shape[:2]
    x = torch.from_numpy(transform(frame)[0]).permute(2, 0, 1)
    x = Variable(x.unsqueeze(0))
    y = net(x)  # forward pass

    detections = y.data
    # scale each detection back up to the image
    scale = torch.Tensor([width, height, width, height])
    for i in range(detections.size(1)):
        j = 0
        while detections[0, i, j, 0] >= 0.6:
            pt = (detections[0, i, j, 1:] * scale).cpu().numpy()
            cv2.rectangle(frame,
                          (int(pt[0]), int(pt[1])),
                          (int(pt[2]), int(pt[3])),
                          COLORS[i % 3], 2)
            cv2.putText(frame, labelmap[i - 1], (int(pt[0]), int(pt[1])),
                        FONT, 2, (255, 255, 255), 2, cv2.LINE_AA)
            j += 1
    return frame


def ssd_net_init(trained_net_name):

    # path of pretrained network
    state_dict = './checkpoints/'+trained_net_name

    # build the net
    net = build_ssd("test",300,21)

    # load model
    net.load_state_dict(torch.load(state_dict))
    return net

def single_model_predict(net_name):
    print('Using model: ', net_name)
    net = ssd_net_init(net_name)
    transform = BaseTransform(net.size, (104/256.0, 117/256.0, 123/256.0))
    return get_predicts(net.eval(), transform)

def muti_model_predict():
    pass

def predict(mode):
    if mode == 'muti':
        return muti_model_predict()
    elif mode == 'single':
        return single_model_predict(SINGLE_NET_NAME)

if __name__ == '__main__':
    predict('single')

