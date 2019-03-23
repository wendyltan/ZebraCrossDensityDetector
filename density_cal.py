#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2019/3/10 14:58
# @Author  : wendy
# @Usage   : For weight definition and density calculation
# @File    : density_cal.py
# @Software: PyCharm
import json
import os
from config import Config as C
from model import Weight
import predictor as pd
from model.Zebra import Zebra
import draw_chart as dc

C = C()

def core_density(zebra_type,predictions,density):
    '''
    Core density calculation
    :param zebra_type:
    :param predictions:
    :param density:
    :return:
    '''
    if density == {}:
        flag = True
    else:
        flag = False
    for image, result in predictions.items():
        if flag:
            density[image] = 0
        if result != {}:
            for type, number in result.items():
                w = Weight.Weight(type).get_weight()
                if type != 'bus' and type != 'car' and zebra_type == 'one_zebra':
                    density[image] += w * number
                elif type != 'bus' and type != 'car' and zebra_type != 'one_zebra':
                    density[image] -= w * number
                elif type == 'bus' or type == 'car' and zebra_type != 'one_zebra':
                    density[image] += w * number

    for image in density:
        if zebra_type == 'tri_zebra' and flag == False:
            density[image] *= 3
        elif zebra_type == 'rec_zebra' and flag ==False:
            density[image] *= 4
        else:
            break

    return density

def single_model_caculation(zebra,predictions):
    '''
    Single model density caculate
    :param zebra_type:
    :param predictions:
    :return:
    '''

    density = {}
    zebra_type = zebra.get_type()
    if zebra_type == 'one_zebra':
        density = core_density(zebra_type,predictions,density)
    elif zebra_type == 'tri_zebra' or zebra_type == 'rec_zebra':
        people = predictions['people']
        cars = predictions['cars']
        # caculate the cars density then substract the people density
        people_density = core_density(zebra_type,people,density)
        density = core_density(zebra_type, cars, people_density)


    return density

def muti_model_caculation(zebra,predictions):
    '''
    Mutiple models density caculate
    :param zebra_type:
    :param predictions:
    :return:
    '''

    muti_density = {}
    model_num = 0
    for model, result in predictions.items():
        for image,result in single_model_caculation(zebra,result).items():
            muti_density[image] = 0
            muti_density[image] += result
        model_num +=1

    for image in muti_density:
        if muti_density[image] !=0:
            muti_density[image] /= model_num
            muti_density[image]=round(muti_density[image],3)

    return muti_density,model_num


def zebra_cross(predictions,zebra):
    '''
    Get density caculation result and check if too crowded
    :param mode:
    :param predictions:
    :param zebra:
    :return:
    '''
    result_set = {}
    mode = zebra.get_mode()
    if mode == 'single':
        result_set = single_model_caculation(zebra,predictions)
        model_num = 1
    elif mode == 'muti':
        result_set,model_num = muti_model_caculation(zebra,predictions)
    print(result_set)
    dc.draw(result_set, zebra,model_num)
    for image,density in result_set.items():
        if zebra.is_over_max(density,model_num):
            result_set[image] = str(density) +' over_max'
            print(image,'density over max!too crowded around')
    write_density(result_set)



def get_predictions(zebra,image_or_video,image_path):
    '''
    Get the predictions from detect and unpack
    :param zebra:
    :return:
    '''
    mode = zebra.get_mode()
    type = zebra.get_type()
    predictions = {}
    # currently only support image mode

    result = pd.predict(zebra, image_or_video,image_path)

    # unpack predict result
    if mode == 'muti':
        for model, prediction in result.items():
            pre = {}
            if image_path !='':
                predictions[model] = prediction.read_predict_result()
            else:
                for class_name, predict in prediction.items():
                    pre[class_name] = predict.read_predict_result()
                predictions[model] = pre
    elif mode == 'single':
        if type == 'one_zebra':
            dic = result.read_predict_result()
            for name, predict in dic.items():
                predictions[name] = predict
        elif type == 'tri_zebra' or type == 'rec_zebra':
            for name,predict in result.items():
                predictions[name] = predict.read_predict_result()

    return predictions

def write_density(result):

    if not os.path.exists(C.PREDICT_RESULT_PATH):
        os.makedirs(C.PREDICT_RESULT_PATH)

    preObj = json.dumps(result)
    fileObject = open(C.PREDICT_RESULT_PATH+'final_result.json', 'w')
    fileObject.write(preObj)
    fileObject.close()

if __name__ == '__main__':
    pass

