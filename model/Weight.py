#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2019/3/10 15:04
# @Author  : wendy
# @Usage   : Weight object for weight info storing and caculating later
# @File    : Weight.py
# @Software: PyCharm
TYPE = ['person','motorbike','bicycle','dog','cat','car','bus']
PERSON_WEIGHT = 1
BIKE_WEIGHT = 1.5
PET_WEIGHT = 0.5
CAR_WEIGHT = 2
class Weight(object):

    def __init__(self,name):
        self.name = name
        if name == TYPE[0]:
            self.weight = PERSON_WEIGHT
        elif name == TYPE[1] or name == TYPE[2]:
            self.weight = BIKE_WEIGHT
        elif name == TYPE[3] or name == TYPE[4]:
            self.weight = PET_WEIGHT
        elif name == TYPE[5] or name == TYPE[6]:
            self.weight = CAR_WEIGHT

    def get_weight(self):
        return self.weight


