#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2019/3/11 11:51
# @Author  : wendy
# @Usage   : The zebra object tends to deal with zebra cross infos
# @File    : Zebra.py
# @Software: PyCharm

# suit yourself to define the max
from config import Config as C
config = C()
MAX_ALLOWED_DENSITY_ONE_ZEBRA = int(config.MAX_ALLOWED_DENSITY_ONE_ZEBRA)
MAX_ALLOWED_DENSITY_TRIANGLE_ZEBRA = int(config.MAX_ALLOWED_DENSITY_TRIANGLE_ZEBRA)
MAX_ALLOWED_DENSITY_RECTANGLE_ZEBRA = int(config.MAX_ALLOWED_DENSITY_RECTANGLE_ZEBRA)

class Zebra(object):

    def __init__(self,cross_type):
        if cross_type == 'one_zebra':
            self.type = 'one_zebra'
            self.name = 'one zebra crossing'
            self.max_density = MAX_ALLOWED_DENSITY_ONE_ZEBRA
        elif cross_type == 'tri_zebra':
            self.type = 'tri_zebra'
            self.name = 'triangle zebra crossing'
            self.max_density = MAX_ALLOWED_DENSITY_TRIANGLE_ZEBRA
        elif cross_type == 'rec_zebra':
            self.type = 'rec_zebra'
            self.name = 'rectangle zebra crossing'
            self.max_density = MAX_ALLOWED_DENSITY_RECTANGLE_ZEBRA


    def is_one_zebra(self):
        if self.type == 'one_zebra':
            return True
        elif self.type == 'tri_zebra' or self.type == 'rec_zebra':
            return False
        else:
            print('ILLEGAL ZEBRA TYPE(one_zebra/tri_zebra/rec_zebra')
            return None

    def get_type(self):
        return self.type
    def get_name(self):
        return self.name

    def get_current_max_density(self):
        return self.max_density

    def is_over_max(self,density,model_num):
        if density > self.get_current_max_density()/model_num:
            return True
        else:
            return False

