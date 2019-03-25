#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2019/3/25 10:22
# @Author  : wendy
# @Usage   : Use this file to auto prepare for running environment
# @File    : auto_prepare.py
# @Software: PyCharm
import os
import shutil
import utils.helper as hp

def copy_files(src_dir, dest_dir):
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)

    count = 0
    for item in os.listdir(src_dir):
        abs_item = os.path.join(src_dir, item)
        dst_name = os.path.join(dest_dir, item)
        if os.path.exists(abs_item):
            count += 1
            shutil.copy(abs_item, dst_name)

        if count >= 20000:
            break
    print("All done")


def rename_all_images(src_dir):
    i = 0
    for file in os.listdir(src_dir):
        if os.path.isfile(os.path.join(src_dir, file)) == True:
            i += 1
            new_name = str(i) + '.jpg'
            os.rename(os.path.join(src_dir, file), os.path.join(src_dir, new_name))
            print(file, 'ok')
    print('All done')

def rename_video(video_path,type):
    video_path = video_path.replace('\\','\\\\')
    src_dir = os.path.dirname(video_path)
    file = os.path.basename(video_path)
    new_name = ''
    if os.path.isfile(os.path.join(src_dir, file)) == True:
        if type == '1':
            new_name = 'cars.mp4'
        elif type == '2':
            new_name = 'people.mp4'
        os.rename(os.path.join(src_dir, file), os.path.join(src_dir, new_name))
        print(file, 'ok')


def dfs_showdir(path, depth):
    if depth == 0:
        print("root:[" + path + "]")

    for item in os.listdir(path):
        if '.git' not in item:
            print("|      " * depth + "+--" + item)

            newitem = path +'/'+ item
            if os.path.isdir(newitem):
                dfs_showdir(newitem, depth +1)


if __name__ == '__main__':
    print('$Auto preparing for basic running environment..')
    hp.mkdir('my_dataset')
    hp.mkdir('my_dataset/video')
    hp.mkdir('my_dataset/zebra_cars')
    hp.mkdir('my_dataset/zebra_people')
    command = input('$Give command: 1(rename images)2(copy files)3(rename video)q(quit)>>')
    while command != 'q':
        if command == '1':
            directory = input('$Give the abs path of the image directory:>>')
            rename_all_images(directory)
        elif command == '2':
            src_dir = input('$Give the source directory of files:>>')
            dest_dir = ''
            type = input('$Give the type of files:1(cars images)2(people images)3(video)/>>')
            if type == '1':
                dest_dir = 'my_dataset/zebra_cars'
            elif type == '2':
                dest_dir = 'my_dataset/zebra_people'
            elif type == '3':
                dest_dir = 'my_dataset/video'

            copy_files(src_dir,dest_dir)
        elif command == '3':
            video_path = input('$Give the abs path of the video path include video name:>>')
            type = input('$Is this a cars or people video?1(cars)2(people)>>')
            rename_video(video_path,type)
        command = input('$Give command: 1(rename images)2(copy files)3(rename video)q(quit)>>')

    dfs_showdir('my_dataset/',0)
    print('$Thanks for using auto_prepare.py!')
