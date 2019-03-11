#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2019/3/10 14:58
# @Author  : wendy
# @Usage   : For weight definition and density calculation
# @File    : density_cal.py
# @Software: PyCharm
from model import Weight
import image_predict as im
from model.Zebra import Zebra


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

def single_model_caculation(zebra_type,predictions):
    '''
    Single model density caculate
    :param zebra_type:
    :param predictions:
    :return:
    '''

    density = {}
    if zebra_type == 'one_zebra':
        density = core_density(zebra_type,predictions,density)
    elif zebra_type == 'tri_zebra' or zebra_type == 'rec_zebra':
        people = predictions['people']
        cars = predictions['cars']
        # caculate the cars density then substract the people density
        people_density = core_density(zebra_type,people,density)
        density = core_density(zebra_type, cars, people_density)


    return density

def muti_model_caculation(zebra_type,predictions):
    '''
    Mutiple models density caculate
    :param zebra_type:
    :param predictions:
    :return:
    '''

    muti_density = {}
    model_num = 0
    for model, result in predictions.items():
        for image,result in single_model_caculation(zebra_type,result).items():
            muti_density[image] = 0
            muti_density[image] += result
        model_num +=1

    for image in muti_density:
        if muti_density[image] !=0:
            muti_density[image] /= model_num
            muti_density[image]=round(muti_density[image],3)

    return muti_density


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
        result_set = single_model_caculation(zebra.get_type(),predictions)
    elif mode == 'muti':
        result_set = muti_model_caculation(zebra.get_type(),predictions)
    print(result_set)

    for image,density in result_set.items():
        if zebra.is_over_max(density):
            print(image,'density over max!too crowded around')


if __name__ == '__main__':
    zebra = Zebra('tri_zebra','muti')
    print('Applying scene: ', zebra.get_name(), '.Using mode:', zebra.get_mode())
    zebra_cross(im.predict(zebra), zebra)
