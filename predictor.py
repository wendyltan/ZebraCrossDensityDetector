#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/10 14:59
# @Author  : wendy
# @Usage   : Recognize images and give prediction result
# @File    : predictor.py
# @Software: PyCharm
import os
import cv2
import torch
from torch.autograd import Variable
from model.Predictions import Predictions
from utils import helper as hp
from train_data import BaseTransform, VOC_CLASSES as labelmap
from traning.ssd import build_ssd
from model.Config import Config as C

C = C()

def predict(pe):
    """
    Start predict with single or multiple model
    :param pe: program entity
    :return:
    """

    if not pe.is_current_model_single():
        return muti_model_predict(pe)
    elif pe.is_current_model_single():
        return single_model_predict(pe,C.SINGLE_NET_NAME)

def single_model_predict(pe,net_name):
    '''
    Make predictions with single model
    :param pe: program entity
    :param net_name: Given ssd network name
    :return: a dictionary of the prediction
    '''
    print('Using model: ', net_name)
    net = ssd_net_init(net_name)
    transform = BaseTransform(net.size, (104, 117, 123))
    pe.set_transform_and_net(transform,net.eval())
    pe.set_model_name(net_name)
    return get_predicts(pe)

def muti_model_predict(pe):
    '''
    Make predictions with multiple models and use thier average.Based on single predict.
    :param pe: program entity
    :return: a two-dimension dictionary of each model's prediction
    '''
    path = C.NET_POSITION
    models = os.listdir(path)  # 得到文件夹下的所有文件名称
    total_dict = {}
    for model in models:  # 遍历文件夹
        total_dict[model] = single_model_predict(pe,model)
        print('Predict with model',model,' end.')
        print('-' * 100)
    print('All predictions complete.')
    return total_dict

def get_predicts(pe):
    """
    Get predict according to the type of zebra cross
    :param pe: program entity
    :return: predict result dictionary
    """

    tag = ['people','cars']
    total = {}
    zebra = pe.get_zebra()

    if zebra.is_one_zebra():
        dir = pe.get_image_source_path(tag[0])

        total = core_predict(dir,tag[0],pe)
    elif not zebra.is_one_zebra():
        # considering the influence of car of the crowd
        print('Do the prediction of people first...')
        print('*' * 100 + '>')
        dir = pe.get_image_source_path(tag[0])
        total['people'] = core_predict(dir,tag[0],pe)

        print('Now doing the predictions of cars...')
        print('*' * 100 + '>')
        dir = pe.get_image_source_path(tag[1])
        total['cars'] = core_predict(dir,tag[1],pe)

    return total

def core_predict(directory,tag,pe):

    """
    Core prediction of images
    :param directory: image source directory
    :param tag: people images or cars images
    :param pe: program entity
    :return:
    """

    # path used for storing predictions results
    result_path = C.DEFAULT_RESULT_PATH
    if pe.get_zebra().is_one_zebra():
        hp.remake_dir(result_path)
    # init the failed count
    failed_count = 0
    image_path = pe.get_image_path()
    transform = pe.get_transform()
    net = pe.get_net()
    model_name = pe.get_model_name()

    if image_path != '' and directory == '':
        image_numbers = 1
    else:
        image_numbers = len(os.listdir(directory))
    predict = None

    for i in range(image_numbers):

        # read in a pic

        if image_path != '' and directory == '':
            img = cv2.imread(image_path, cv2.IMREAD_COLOR)
            img_name = os.path.basename(image_path)
        else:
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
        predict = Predictions(img_name,tag,model_name)


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
                              C.COLORS[i % 3], 2)
                cv2.putText(img, label_name, (int(pt[0]), int(pt[1])),
                            C.FONT, 0.8, (255, 255, 255), 1, cv2.LINE_AA)
                cv2.imwrite(result_path + '/result_' + tag+'_'+img_name, img)

                pred_num += 1
                print(str(pred_num) + ' ' + label_name + ' , score: ' +
                      str(score) + ' position: ' + ' || '.join(str(c) for c in coords))
                predict.type_identify(label_name)
                j += 1


        predict.write_predict_result('w')
        if not predict.get_predict_flag():
            failed_count += 1

    if image_path != '':
        predict.write_total_predict(os.path.basename(image_path))
    else:
        predict.write_total_predict(image_numbers)
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



