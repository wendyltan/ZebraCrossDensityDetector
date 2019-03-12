#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/10 14:59
# @Author  : wendy
# @Usage   : The predictions of image mode
# @File    : predictor.py
# @Software: PyCharm
import os
from time import sleep

import cv2
import torch
from torch.autograd import Variable
from model.Predictions import Predictions
from utils import helper as hp
from data import BaseTransform, VOC_CLASSES as labelmap
from ssd import build_ssd



COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
FONT = cv2.FONT_HERSHEY_SIMPLEX
# using author's best trained model as default
SINGLE_NET_NAME = 'ssd300_mAP_77.43_v2.pth'
NET_POSITION = './checkpoints'
DEFAULT_RESULT_PATH = 'my_dataset/result'
MAX_SAVED_IMAGE = 10
SLEEP_TIME = 5


def predict(zebra,image_or_video):
    '''
    Make predictions according to the zebra cross type and mode
    :param cross_type: one_zebra,tri_zebra or rec_zebra
    :param mode: single or muti
    :return:
    '''
    mode = zebra.get_mode()
    cross_type = zebra.get_type()
    if mode == 'muti':
        return muti_model_predict(cross_type,image_or_video)
    elif mode == 'single':
        return single_model_predict(cross_type,SINGLE_NET_NAME,image_or_video)

def single_model_predict(cross_type,net_name,image_or_video):
    '''
    Make predictions with single model
    :param cross_type: one_zebra,tri_zebra or rec_zebra
    :param net_name: Given ssd network name
    :return: a dictionary of the prediction
    '''
    print('Using model: ', net_name)
    net = ssd_net_init(net_name)
    transform = BaseTransform(net.size, (104, 117, 123))
    return get_predicts(cross_type,transform, net.eval(),image_or_video)

def muti_model_predict(cross_type,image_or_video):
    '''
    Make predictions with multiple models and use thier average.Based on single predict.
    :param cross_type:  one_zebra,tri_zebra or rec_zebra
    :return: a two-dimension dictionary of each model's prediction
    '''
    path = NET_POSITION
    models = os.listdir(path)  # 得到文件夹下的所有文件名称
    total_dict = {}
    for model in models:  # 遍历文件夹
        total_dict[model] = single_model_predict(cross_type,model,image_or_video)
        print('Predict with model',model,' end.')
        print('-' * 100)
    print('All predictions complete.')
    return total_dict

def get_predicts(cross_type, transform, net,image_or_video):

    '''
    Rely on core_predict
    :param cross_type:
    :param net:
    :param transform:
    :return:
    '''
    tag = ['people','cars']
    total = {}
    if cross_type == 'one_zebra':
        path = judge_mode(image_or_video, tag[0])
        total = core_predict(path, transform, net, tag[0])
    elif cross_type == 'tri_zebra' or cross_type == 'rec_zebra':
        # considering the influence of car of the crowd
        print('Do the prediction of people first...')
        print('*' * 100 + '>')
        path = judge_mode(image_or_video, tag[0])
        total['people'] = core_predict(path, transform, net, tag[0])

        print('Now doing the predictions of cars...')
        print('*' * 100 + '>')
        path = judge_mode(image_or_video, tag[1])
        total['cars'] = core_predict(path, transform, net, tag[1])
    return total


def judge_mode(image_or_video,tag):
    path = ''
    if image_or_video == 'image':
        base_dir = 'my_dataset/zebra_'
        path = base_dir+tag
        hp.mkdir(path)
    elif image_or_video == 'video':
        base_dir = 'my_dataset/video_'
        path = base_dir+tag
        hp.mkdir(path)
        image_capture(path)
    return path

def image_capture(saveDir):
    # start image capturing
    image_Count = 1
    cap = cv2.VideoCapture(0)
    width, height = 640, 480
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    print('width: ', width)
    print('height: ', height)


    while True:

        ret, frame = cap.read()
        frame = cv2.flip(frame, 1, dst=None)
        key = cv2.waitKey(1) & 0xFF
        cv2.imshow("video_detect", frame)
        # save original image
        cv2.imwrite("%s/%d.jpg" % (saveDir, image_Count), cv2.resize(frame, (300, 300), interpolation=cv2.INTER_AREA))
        print(u"%s:第 %d 张图片" % (saveDir, image_Count))
        # do frame predict and save detect result image to result/
        if key == 27 or image_Count == MAX_SAVED_IMAGE:  # exit
            break
        image_Count += 1

        # save pic every 5 seconds
        sleep(SLEEP_TIME)

    cap.release()  # 释放摄像头
    cv2.destroyAllWindows()  # 丢弃窗口



def core_predict(directory,transform,net,tag):
    '''
    Core code of predictions
    :param directory: directory to be read
    :param transform:
    :param net:
    :param tag: people or cars
    :return:
    '''

    # path used for storing predictions results
    result_path = DEFAULT_RESULT_PATH
    hp.mkdir(result_path)
    # init the failed count
    failed_count = 0
    total_prediction = {}
    image_numbers = len(os.listdir(directory))
    predict = None


    for i in range(image_numbers):

        # read in a pic
        img = hp.pull_image(directory, i + 1)
        img_name = str(i + 1) + '.jpg'

        # core code of image content prediction
        x = torch.from_numpy(transform(img)[0]).permute(2, 0, 1)
        x = Variable(x.unsqueeze(0))

        y = net(x)  # forward pass
        detections = y.data

        # get height and width of the image
        height = img.shape[0]
        width = img.shape[1]

        scale = torch.Tensor([width, height, width, height])

        pred_num = 0
        predict = Predictions(img_name,tag)

        for i in range(detections.size(1)):
            j = 0
            while detections[0, i, j, 0] >= 0.6:
                if pred_num == 0:
                    print("predictions of ", img_name)
                predict.set_predict_flag(True)

                score = detections[0, i, j, 0]
                label_name = labelmap[i - 1]
                pt = (detections[0, i, j, 1:] * scale).cpu().numpy()
                coords = (pt[0], pt[1], pt[2], pt[3])

                # use cv2 to draw bounding box of detections
                cv2.rectangle(img,
                              (int(pt[0]), int(pt[1])),
                              (int(pt[2]), int(pt[3])),
                              COLORS[i % 3], 2)
                cv2.putText(img, label_name, (int(pt[0]), int(pt[1])),
                            FONT, 0.8, (255, 255, 255), 1, cv2.LINE_AA)
                cv2.imwrite(result_path + '/result_' + tag+'_'+img_name, img)

                pred_num += 1
                print(str(pred_num) + ' it should be ' + label_name + ' , score: ' +
                      str(score) + ' detect position: ' + ' || '.join(str(c) for c in coords))
                predict.type_identify(label_name)
                j += 1


            predict.write_predict_result()

        if not predict.get_predict_flag():
            failed_count += 1
        predict.set_total_predict(total_prediction)

    print('-' * 100)
    print(failed_count, 'of the images detect failed,total ', image_numbers, ' of images for dataset ',directory)
    print('-' * 100)
    return predict

def ssd_net_init(trained_net_name):
    '''
    Init the ssd pre-trained network
    :param trained_net_name:
    :return:
    '''

    # path of pretrained network
    state_dict = './checkpoints/'+trained_net_name

    # build the net
    net = build_ssd("test",300,21)

    # load model
    net.load_state_dict(torch.load(state_dict))

    return net


def read_video_and_predict():
    # wait to be implemented
    pass

