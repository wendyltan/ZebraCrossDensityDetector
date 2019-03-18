#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2019/3/13 10:40
# @Author  : wendy
# @Usage   : Set some global config here
# @File    : config.py
# @Software: PyCharm
import cv2
import configparser

class Config(object):
    def __init__(self):
        self.COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
        self.FONT = cv2.FONT_HERSHEY_SIMPLEX
        self.read_config_file()

    def write_config_file(self,section,key,new_value):
        conf = configparser.ConfigParser()
        conf.set(section,key,new_value)
        conf.write(open("config.ini", "w"))

    def read_config_file(self):
        conf = configparser.ConfigParser()
        conf.read("config.ini")
        # do global setting
        self.SINGLE_NET_NAME = conf.get("global setting", "single_net_name")
        self.NET_POSITION = conf.get("global setting", "net_position")
        self.DEFAULT_VIDEO_SOURCE = conf.get("global setting","default_video_source")
        self.ICON_PATH = conf.get("global setting","icon_path")
        self.DEFAULT_RESULT_PATH = conf.get("global setting","default_result_path")
        self.MAX_SAVED_IMAGE = conf.get("global setting","max_saved_image")
        self.PREDICT_RESULT_PATH = conf.get("global setting","predict_result_path")
        self.PREDICT_RESULT_IMAGE = conf.get("global setting","predict_result_image")
        # do weight setting
        self.PERSON_WEIGHT = conf.get("weight setting","person_weight")
        self.BIKE_WEIGHT = conf.get("weight setting","bike_weight")
        self.PET_WEIGHT = conf.get("weight setting","pet_weight")
        self.CAR_WEIGHT = conf.get("weight setting","car_weight")
        # do max density setting
        self.MAX_ALLOWED_DENSITY_ONE_ZEBRA = conf.get("max density setting","max_allowed_density_one_zebra")
        self.MAX_ALLOWED_DENSITY_TRIANGLE_ZEBRA = conf.get("max density setting","max_allowed_density_triangle_zebra")
        self.MAX_ALLOWED_DENSITY_RECTANGLE_ZEBRA = conf.get("max density setting","max_allowed_density_rectangle_zebra")

