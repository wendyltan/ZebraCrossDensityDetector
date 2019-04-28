#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2019/3/10 14:58
# @Author  : wendy
# @Usage   : Receive prediction result and make density calculation
# @File    : density_cal.py
# @Software: PyCharm
import json
import os

from model.Config import Config as C
from model import Weight, TimeIndicator
import predictor as pd
import draw_chart as dc
import threading

C = C()
T = TimeIndicator.TimeIndicator()
finish = False
val = 0
mutex = threading.Lock()

class DensityThread (threading.Thread):
    """
    Use this thread class to pass progress to MainWindow
    and do predict and caculate work at the same time.
    """
    def __init__(self, pe,threadId):
        threading.Thread.__init__(self)
        self.pe = pe
        self.threadId = threadId
        self.init_file()

    def init_file(self):
        mutex.acquire(10)
        self.f = open('progress_write.txt', 'w')
        self.f.writelines(str(0) + '\n')
        self.f.close()
        mutex.release()

    def run(self):
        global finish
        if self.threadId == 1:
            self.write_progress()
        elif self.threadId == 2:
            predictions = get_predictions(self.pe)
            get_caculations(predictions, self.pe)
            finish = True
        elif self.threadId == 3:
            self.read_progress()

    def write_progress(self):
        i = 0.005
        while finish != True:
            mutex.acquire(10)
            f = open('progress_write.txt', 'w')
            f.writelines(str(i) + '\n')
            i += 0.005
            if i > 100:
                break
            f.close()
            mutex.release()

    def read_progress(self):
        global val
        while finish != True:
            mutex.acquire(10)
            f = open('progress_write.txt', 'r')
            lines = f.readlines()  # 读取所有行
            last_line = lines[0].strip('\n')  # 取最后一行
            val = int(float(last_line))
            if val >= 100:
                break
            f.close()
            mutex.release()

def core_density(zebra_type,predictions,tag):

    """
    Core caculation of density
    :param zebra_type: zebra_cross type
    :param predictions: a dictionary
    :param density: a dictionary,could be empty
    :return:
    """
    density={}
    for image, result in predictions.items():
        if result != {}:
            density[image] = 0
            for type, number in result.items():
                w = Weight.Weight(type).get_weight()
                if T.if_gaofeng():
                    # car first
                    if tag == 'people' and type != 'bus' and type != 'car':
                        density[image] -= w * number
                    elif tag == 'cars' and (type == 'bus' or type == 'car'):
                        density[image] += w * number
                else:
                    # people first
                    if tag == 'people' and type != 'bus' and type != 'car':
                        density[image] += w * number
                    elif tag == 'cars' and (type == 'bus' or type == 'car'):
                        density[image] -= w * number

    for image in density:
        if zebra_type == 'tri_zebra':
            density[image] *= 3
        elif zebra_type == 'rec_zebra':
            density[image] *= 4
        density[image] = round(density[image],2)

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
        density = core_density(zebra_type,predictions,'people')
    elif not zebra.is_one_zebra():
        people = predictions['people']
        cars = predictions['cars']
        # caculate the cars density then substract the people density
        people_density = core_density(zebra_type,people,'people')
        print('people density',people_density)
        car_density = core_density(zebra_type, cars, 'cars')
        print('car density',car_density)

        for image,cal in people_density.items():
            density[image] = 0
            density[image] += cal
        for image,cal in car_density.items():
            density[image] += cal
            density[image] = round(density[image],2)

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
    flag = False
    for model, result in predictions.items():
        for image,result in single_model_caculation(zebra,result).items():
            if not flag:
                muti_density[image] = 0
            muti_density[image] += result
            print(image,result)
        flag = True
        print('=====')
        model_num +=1

    for image in muti_density:
        if muti_density[image] !=0:
            muti_density[image] /= model_num
            muti_density[image]=round(muti_density[image],2)

    return muti_density


def get_caculations(predictions, pe):
    """
    Get caculation result and write into files,draw on chart.
    :param predictions: predictions dictionary
    :param pe: program entity
    :return:
    """

    result_set = {}
    zebra = pe.get_zebra()

    if pe.is_current_model_single():
        result_set = single_model_caculation(zebra,predictions)
    elif not pe.is_current_model_single():
        result_set = muti_model_caculation(zebra,predictions)
    print("Final result of density caculation: ",result_set)

    dc.draw(result_set,zebra)

    for image,density in result_set.items():
        if zebra.is_over_max(density):
            print(image,'density too big! current density is ',density,T.who_go_first())
        else:
            print(image,'current density is ',density,T.who_wait())

    write_density(result_set)

    # single image detect don't do the density adjust.
    if not pe.get_image_path() != '':
        adjust_max_density(zebra,result_set)


def adjust_max_density(zebra,result_set):
    """
    Adjust max density by getting group images' density average to better fit next start
    :param zebra:
    :param result_set:
    :return:
    """
    sum = count = 0

    for image,density in result_set.items():
        sum += density
        count +=1
    # get average
    sum /= count
    max_density = zebra.get_max_type()
    current_max = zebra.get_current_max_density(max_density)
    new_current_max = 0

    while True:
        if not round(new_current_max,1) == current_max:
            print('Do max_density adjust,new max at next start.')
            zebra.reload_config()
            current_max = zebra.get_current_max_density(max_density)
            new_current_max = (current_max + sum) / 2
            zebra.set_current_max_density(max_density,str(round(new_current_max,1)))
        else:
            print("Adjust current max_density:",str(round(new_current_max,1)))
            break


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
                if zebra.is_one_zebra():
                    pack1 = prediction.read_predict_result()
                    for class_name, predict in pack1.items():
                        pre[class_name] = predict
                elif not zebra.is_one_zebra():
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

def start_caculate(pe):
    writeThread = DensityThread(pe,1)
    workThread = DensityThread(pe,2)
    readThread = DensityThread(pe,3)
    writeThread.start()
    workThread.start()
    readThread.start()
