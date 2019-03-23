#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2019/3/12 11:31
# @Author  : wendy
# @Usage   : Saving the common used function.
# @File    : helper.py
# @Software: PyCharm
import inspect
import os
import cv2
from PIL import Image


def pull_image(directory,index):

    '''
    Return the right format that the net can use to predict.
    :param directory: image directory
    :param index: the index of each image
    :return:
    '''
    file_path = directory + '/'+str(index) + '.jpg'
    image_resize(file_path)

    # can not accept Chinese file path!
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

def mkdir(path):
    '''
    Make a new directory to store result pictures
    :param path:
    :return:
    '''
    if not os.path.exists(path):
        os.makedirs(path)
        print('make result directory success')

def load_file(relative_path):

    current_path = inspect.getfile(inspect.currentframe())
    dir_name = os.path.dirname(current_path)
    file_abs_path = os.path.abspath(dir_name)
    list_path = os.path.split(file_abs_path)
    file_path = os.path.join(list_path[0], relative_path)

    return file_path

def get_latest_file(relative_dir):
    list = os.listdir(relative_dir)
    list.sort(key=lambda fn: os.path.getmtime(relative_dir + fn)
    if not os.path.isdir(relative_dir + fn) else 0)
    return list[-1]
