#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2019/3/13 11:22
# @Author  : wendy
# @Usage   : Use prediction final result to drawchart
# @File    : draw_chart.py
# @Software: PyCharm

import plotly.graph_objs as go
import plotly.offline as off
from config import Config as C
from utils import helper as hp

C = C()
def draw(result_set,zebra,model_num):

    print('Ploting the image now...')
    plot_dir = C.PREDICT_RESULT_IMAGE
    hp.mkdir(plot_dir)
    save_name = zebra.get_name()
    x_list = []
    y_list = []
    max_list = []

    for name,result in result_set.items():
        x_list.append(name)
        y_list.append(result)
        max_list.append(round(zebra.get_current_max_density()/model_num,2))

    print('Saving html image under ',plot_dir)
    draw_line_plot(x_list,y_list,max_list,save_name,plot_dir)


def draw_line(list_x,list_y,name):
    trace= go.Scatter(
        x=list_x,
        y=list_y,
        mode='lines',
        name= name
    )
    return trace
def draw_line_with_markers(list_x,list_y,name):
    trace = go.Scatter(
        x=list_x,
        y=list_y,
        mode='lines+markers',
        name= name
    )
    return trace

def draw_line_plot(list_x,list_y,max_list,title,save_dir):

    trace1 = draw_line(list_x,list_y,'result_density')
    trace2 = draw_line_with_markers(list_x,max_list,'max_density')
    data = [trace1,trace2]
    off.plot(data,filename=save_dir+title+'.html',auto_open=False)
