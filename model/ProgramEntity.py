#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2019/3/27 9:43
# @Author  : wendy
# @Usage   : The object to store the basic parameters to make program run
# @File    : ProgramEntity.py
# @Software: PyCharm
class ProgramEntity(object):
    def __init__(self,zebra,current_mode,image_path,current_model):
        self.zebra = zebra
        self.current_mode = current_mode
        self.image_path = image_path
        self.current_model = current_model

    def get_zebra(self):
        return self.zebra

    def get_current_mode(self):
        return self.current_mode

    def get_image_path(self):
        return self.image_path

    def get_current_model(self):
        return self.current_model

    def is_current_model_single(self):
        if self.current_model == 'single':
            return True
        elif self.current_model == 'muti':
            return False
        else:
            print('ILLEGAL MODEL TYPE(single or muti only)')
            return None

    def set_transform_and_net(self,transform,net):
        self.transform = transform
        self.net = net

    def get_transform(self):
        return self.transform

    def get_net(self):
        return self.net

    def get_image_source_path(self,tag):
        path = ''
        if self.current_mode == 'image':
            base_dir = 'my_dataset/zebra_'
            path = base_dir + tag
        elif self.current_mode == 'video':
            base_dir = 'my_dataset/video_'
            path = base_dir + tag
        if self.image_path!='':
            path = ''
        return path
