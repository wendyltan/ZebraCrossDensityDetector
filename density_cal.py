#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2019/3/10 14:58
# @Author  : wendy
# @Usage   : Receive prediction result and make density calculation
# @File    : density_cal.py
# @Software: PyCharm
import json
import os
from config import Config as C
from model import Weight
import predictor as pd
from model.ProgramEntity import ProgramEntity
from model.Zebra import Zebra
import draw_chart as dc

C = C()

def core_density(zebra_type,predictions,density):

    """
    Core caculation of density
    :param zebra_type: zebra_cross type
    :param predictions: a dictionary
    :param density: a dictionary,could be empty
    :return:
    """

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
    """
    Caculate density with single model
    :param zebra: zebra object
    :param predictions: a result dictionary
    :return:
    """

    density = {}
    zebra_type = zebra.get_type()
    if zebra.is_one_zebra():
        density = core_density(zebra_type,predictions,density)
    elif not zebra.is_one_zebra():
        people = predictions['people']
        cars = predictions['cars']

        # caculate the cars density then substract the people density
        people_density = core_density(zebra_type,people,density)
        density = core_density(zebra_type, cars, people_density)

    return density

def muti_model_caculation(zebra,predictions):
    """
    Caculate density with multiple models
    :param zebra: zebra object
    :param predictions: a result dictionary
    :return:
    """

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


def get_caculations(predictions, pe):
    """
    Get caculation result and write into files,draw on chart.
    :param predictions: predictions dictionary
    :param pe: program entity
    :return:
    """

    result_set = {}
    model_num = 1
    zebra = pe.get_zebra()


    if pe.is_current_model_single():
        result_set = single_model_caculation(zebra,predictions)
    elif not pe.is_current_model_single():
        result_set,model_num = muti_model_caculation(zebra,predictions)

    print("Final result of density caculation: ",result_set)

    dc.draw(result_set,zebra,model_num)

    for image,density in result_set.items():
        if zebra.is_over_max(density,model_num):
            print(image,'density over max!too crowded around')

    write_density(result_set)



def get_predictions(pe):
    """
    Get prediction result from predictor module
    :param pe: program entity
    :return:
    """

    result = pd.predict(pe)
    predictions = unpack_predict(result,pe)
    print("Final predictions of all images: ", predictions)

    return predictions

def unpack_predict(result,pe):
    """
    Unpack prediction result and read from pre-saved files
    :param result: prediction dictionary packed by Predictions objects
    :param pe: program entity
    :return:
    """

    zebra = pe.get_zebra()
    image_path = pe.get_image_path()

    predictions = {}
    if not pe.is_current_model_single():
        for model, prediction in result.items():
            pre = {}
            if image_path != '':
                predictions[model] = prediction.read_predict_result()
            else:
                for class_name, predict in prediction.items():
                    pre[class_name] = predict.read_predict_result()
                predictions[model] = pre
    elif pe.is_current_model_single():
        if zebra.is_one_zebra():
            dic = result.read_predict_result()
            for name, predict in dic.items():
                predictions[name] = predict
        elif not zebra.is_one_zebra():
            for name, predict in result.items():
                predictions[name] = predict.read_predict_result()

    return predictions

def write_density(result):

    """
    write result into json file format
    :param result:
    :return:
    """

    if not os.path.exists(C.PREDICT_RESULT_PATH):
        os.makedirs(C.PREDICT_RESULT_PATH)

    preObj = json.dumps(result)
    fileObject = open(C.PREDICT_RESULT_PATH+'final_result.json', 'w')
    fileObject.write(preObj)
    fileObject.close()

if __name__ == '__main__':
    zebra = Zebra('one_zebra')
    pe = ProgramEntity(zebra,'image','','single')
    print('Applying scene: ', zebra.get_name(), '.Using model:',pe.get_current_model())
    predictions = get_predictions(pe)
    get_caculations(predictions, pe)
