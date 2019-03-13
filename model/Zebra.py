#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2019/3/11 11:51
# @Author  : wendy
# @Usage   : 
# @File    : Zebra.py
# @Software: PyCharm

# suit yourself to define the max
MAX_ALLOWED_DENSITY_ONE_ZEBRA = 5
MAX_ALLOWED_DENSITY_TRIANGLE_ZEBRA = 10
MAX_ALLOWED_DENSITY_RECTANGLE_ZEBRA = 25
class Zebra(object):

    def __init__(self,cross_type,mode='single'):
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
        self.mode = mode

    def get_type(self):
        return self.type
    def get_name(self):
        return self.name

    def get_mode(self):
        return self.mode

    def set_mode(self,mode):
        if mode!='single' and mode != 'muti':
            print('Mode can only be single or muti!')
        else:
            self.mode = mode


    def get_current_max_density(self):
        return self.max_density

    def set_max_density(self,new_density):
        self.max_density = new_density
        print('Now the max density of ',self.get_name(),' is ',self.get_current_max_density())

    def is_over_max(self,density):
        if density > self.get_current_max_density():
            return True
        else:
            return False

