#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2019/3/12 11:15
# @Author  : wendy
# @Usage   : 
# @File    : Predictions.py
# @Software: PyCharm
import os
import json
from config import Config as C
PREDICT_RESULT_PATH = C().PREDICT_RESULT_PATH

class Predictions(object):
    '''
    Class that deal with predict data saving and reading
    '''

    def __init__(self,image_name,type):
        self.image_name = image_name
        self.result = self.init_prediction_result()
        self.flag = False
        self.type = type
        self.save_path = PREDICT_RESULT_PATH+self.image_name+'_'+self.type+'.json'

    def get_image_name(self):
        return self.image_name

    def get_predict_flag(self):
        return self.flag

    def set_predict_flag(self,flag):
        self.flag = flag

    def init_prediction_result(self):
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

    def type_identify(self,label):
        '''
        Identify each type's count in each image.
        :param label: class type name
        :param prediction_result: the predictions result
        :return: the predictions result
        '''
        if label == 'person' or label == 'motorbike' or label == 'bicycle' \
                or label == 'dog' or label == 'cat' \
                or label == 'car' or label == 'bus':
           self.result[label] += 1
        else:
            print('We don\' consider other type in this program')

    def get_predict_result(self):
        return self.result

    def set_total_predict(self,total_prediction):
        '''
        Return the final result of predictions
        :param image_name: image name
        :param total_prediction:
        :param prediction_result:
        :return:
        '''
        total_prediction[self.image_name] = self.result
        self.result = total_prediction
        self.save_path = PREDICT_RESULT_PATH + self.type + '.json'
        self.write_predict_result()

    def write_predict_result(self):
        if not os.path.exists(PREDICT_RESULT_PATH):
            os.makedirs(PREDICT_RESULT_PATH)

        preObj = json.dumps(self.result)

        fileObject = open(self.save_path, 'w')
        fileObject.write(preObj)
        fileObject.close()

    def read_predict_result(self):
        with open(self.save_path, 'r') as f:
            self.result = json.loads(f.read())
        return self.result







