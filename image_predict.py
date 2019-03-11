#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/10 14:59
# @Author  : wendy
# @Usage   : The predictions of image mode
# @File    : image_predict.py
# @Software: PyCharm
import os
from time import sleep

import cv2
import torch
from torch.autograd import Variable
from os import path
from data import BaseTransform, VOC_CLASSES as labelmap
from ssd import build_ssd
from PIL import Image


COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
FONT = cv2.FONT_HERSHEY_SIMPLEX
# using author's best trained model as default
SINGLE_NET_NAME = 'ssd300_mAP_77.43_v2.pth'
NET_POSITION = './checkpoints'
DEFAULT_RESULT_PATH = 'my_dataset/result'

def predict(zebra):
    '''
    Make predictions according to the zebra cross type and mode
    :param cross_type: one_zebra,tri_zebra or rec_zebra
    :param mode: single or muti
    :return:
    '''
    mode = zebra.get_mode()
    cross_type = zebra.get_type()
    if mode == 'muti':
        return muti_model_predict(cross_type)
    elif mode == 'single':
        return single_model_predict(cross_type,SINGLE_NET_NAME)

def single_model_predict(cross_type,net_name):
    '''
    Make predictions with single model
    :param cross_type: one_zebra,tri_zebra or rec_zebra
    :param net_name: Given ssd network name
    :return: a dictionary of the prediction
    '''
    print('Using model: ', net_name)
    net = ssd_net_init(net_name)
    transform = BaseTransform(net.size, (104, 117, 123))
    return get_predicts(cross_type, net.eval(), transform)

def muti_model_predict(cross_type):
    '''
    Make predictions with multiple models and use thier average.Based on single predict.
    :param cross_type:  one_zebra,tri_zebra or rec_zebra
    :return: a two-dimension dictionary of each model's prediction
    '''
    path = NET_POSITION
    models = os.listdir(path)  # 得到文件夹下的所有文件名称
    total_dict = {}
    for model in models:  # 遍历文件夹
        total_dict[model] = single_model_predict(cross_type,model)
        print('Predict with model',model,' end,sleeping 5 seconds...')
        print('-' * 100)
        sleep(5)
    print('All predictions complete.')
    return total_dict


def init_prediction_result():
    '''
    Init the whole prediction result dictionary
    :return:
    '''
    prediction_result = {}
    prediction_result['person'] = 0
    prediction_result['motorbike'] = 0
    prediction_result['bicycle'] = 0
    prediction_result['dog'] = 0
    prediction_result['cat'] = 0
    prediction_result['car'] = 0
    prediction_result['bus'] = 0
    return prediction_result

def type_identify(label,prediction_result):
    '''
    Identify each type's count in each image.
    :param label: class type name
    :param prediction_result: the predictions result
    :return: the predictions result
    '''
    if prediction_result == {}:
        predi_result  = init_prediction_result()
    else:
        predi_result = prediction_result
    if label == 'person' or label == 'motorbike'or label == 'bicycle'\
            or label == 'dog'or label == 'cat'\
            or label == 'car'or label == 'bus':
        predi_result[label] += 1
    else:
        print('We don\' consider other type in this program')
    return predi_result

def total_predict(image_name,total_prediction,prediction_result):
    '''
    Return the final result of predictions
    :param image_name: image name
    :param total_prediction:
    :param prediction_result:
    :return:
    '''
    total_prediction[image_name]=prediction_result
    return total_prediction


def mkdir(path):
    '''
    Make a new directory to store result pictures
    :param path:
    :return:
    '''
    if not os.path.exists(path):
        os.makedirs(path)
        print('make result directory success')
    else:
        print('target directory already satisfied!')


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

def pull_image(directory,index):

    '''
    Return the right format that the net can use to predict.
    :param directory: image directory
    :param index: the index of each image
    :return:
    '''
    file_path = directory + '/'+str(index) + '.jpg'
    image_resize(file_path)
    return cv2.imread(file_path, cv2.IMREAD_COLOR)

def image_resize(file_path):

    '''
    Resize the image before predict,using specific size similiar with VOC training dataset.
    :param file_path:
    :return:
    '''
    im = Image.open(file_path)
    new_x = 500
    new_y = 375
    out = im.resize((new_x, new_y), Image.ANTIALIAS)
    out.save(file_path)

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
    mkdir(result_path)
    # init the failed count
    failed_count = 0
    total_prediction = {}
    image_numbers = len(os.listdir(directory))

    for i in range(image_numbers):

        # read in a pic
        img = pull_image(directory, i + 1)
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
        prediction_result = {}
        predit_flag = False

        for i in range(detections.size(1)):
            j = 0
            while detections[0, i, j, 0] >= 0.6:
                if pred_num == 0:
                    print("predictions of ", img_name)
                predit_flag = True

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
                j += 1

                prediction_result = type_identify(label_name, prediction_result)
        if not predit_flag:
            failed_count += 1
        total_prediction = total_predict(img_name, total_prediction, prediction_result)


    print('-' * 100)
    print(failed_count, 'of the images detect failed,total ', image_numbers, ' of images for dataset ',directory)
    print('-' * 100)
    return total_prediction


def get_predicts(cross_type, net, transform):

    '''
    Rely on core_predict
    :param cross_type:
    :param net:
    :param transform:
    :return:
    '''

    base_dir = 'my_dataset/zebra_'
    tag = ['people','cars']
    if cross_type == 'one_zebra':
        total = core_predict(base_dir+tag[0],transform,net,tag[0])
        return total
    elif cross_type == 'tri_zebra' or cross_type == 'rec_zebra':
        # considering the influence of car of the crowd
        total = {}
        print('Do the prediction of people first...')
        print('*' * 100 + '>')
        total['people'] = core_predict(base_dir+tag[0],transform,net,tag[0])
        print('Now doing the predictions of cars...')
        print('*' * 100 + '>')
        total['cars']= core_predict(base_dir+tag[1],transform,net,tag[1])
        return total


