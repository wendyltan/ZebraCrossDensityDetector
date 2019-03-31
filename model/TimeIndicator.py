#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2019/3/30 18:41
# @Author  : wendy
# @Usage   : 
# @File    : TimeIndicator.py
# @Software: PyCharm
import time
class TimeIndicator(object):

    def __init__(self):
        self.name = self.show_time() + ' time Indicator'
        self.gaofeng = False

    def show_time(self):
        self.current_show_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        return self.current_show_time

    def localtime(self):
        self.time_dic = time.localtime(time.time())
        return self.time_dic

    def if_gaofeng(self):
        current_hour = self.localtime().tm_hour
        current_min = self.localtime().tm_min
        if (current_hour >= 7 and current_min >= 40) and (current_hour <=8 and current_min <=30):
            #7.40~8.30
            self.gaofeng = True
            self.day_or_night = 'am'
        elif (current_hour >= 17 and current_min >=30 )and (current_hour <= 19 and current_min<=30):
            #17.30~19.30
            self.gaofeng = True
            self.day_or_night = 'pm'
        return self.gaofeng

    def who_go_first(self):
        if self.gaofeng:
           return 'Is gaofeng,cars go first'
        else:
           return 'Not gaofeng,people go first.'

    def who_wait(self):
        if self.gaofeng:
            return 'cars wait.'
        else:
            return  'people wait.'

    def get_day_or_night(self):
        current_hour = self.localtime().tm_hour
        if current_hour <= 12:
            self.day_or_night = 'am'
        else:
            self.day_or_night = 'pm'
        return self.day_or_night

