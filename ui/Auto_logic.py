#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2019/3/27 15:37
# @Author  : wendy
# @Usage   : 
# @File    : Auto_logic.py
# @Software: PyCharm
import os
import shutil

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileSystemModel
from utils import helper as hp
from ui.AutoPrepare import Ui_Dialog

class AutoPrepare(QtWidgets.QDialog,Ui_Dialog):
    def __init__(self):
        super(AutoPrepare,self).__init__()
        self.setupUi(self)
        self.setWindowTitle('快速部署')
        self.setFixedSize(639, 592)

        self.chooseImageDir.clicked.connect(self.rename_all_images)
        self.chooseVideo.clicked.connect(self.rename_video)
        self.chooseFile.clicked.connect(self.copy_files)
        self.fileTypeCombo.addItems(['people','cars','video'])
        self.videoTypeCombo.addItems(['people','cars'])
        self.fileTypeCombo.setCurrentText('选择类型')

        self.videoTypeCombo.setCurrentText('选择类型')

        self.make_new_dir()

        self.model = QFileSystemModel()
        self.model.setRootPath('my_dataset/')
        self.dirTreeView.setModel(self.model)
        self.dirTreeView.setAnimated(False)
        self.dirTreeView.setIndentation(20)
        self.dirTreeView.setSortingEnabled(True)
        self.dirTreeView.setRootIndex(self.model.index('my_dataset/'))




    def make_new_dir(self):
        print('$Auto preparing for basic running environment..')
        hp.mkdir('my_dataset')
        hp.mkdir('my_dataset/video')
        hp.mkdir('my_dataset/zebra_cars')
        hp.mkdir('my_dataset/zebra_people')
        hp.mkdir('my_dataset/result')


    def copy_files(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, '打开文件夹', r'my_dataset/')
        if directory != '':
            type = self.fileTypeCombo.currentText()
            self.copy_file_line.setText(directory)
            dest_dir = ''
            if type == 'people':
                dest_dir = 'my_dataset/zebra_people'
            elif type == 'cars':
                dest_dir = 'my_dataset/zebra_cars'
            elif type == 'video':
                dest_dir = 'my_dataset/video'

            if not os.path.exists(dest_dir):
                os.mkdir(dest_dir)
            count = 0
            for item in os.listdir(directory):
                abs_item = os.path.join(directory, item)
                dst_name = os.path.join(dest_dir, item)
                if os.path.exists(abs_item):
                    count += 1
                    shutil.copy(abs_item, dst_name)

                if count >= 20000:
                    break
            print("All done")


    def rename_all_images(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, '打开文件夹', r'my_dataset/')
        if directory != '':
            self.rename_images_line.setText(directory)
            i = 0
            for file in os.listdir(directory):
                if os.path.isfile(os.path.join(directory, file)) == True:
                    i += 1
                    new_name = str(i) + '.jpg'
                    os.rename(os.path.join(directory, file), os.path.join(directory, new_name))
                    print(file, 'ok')
            print('All done')


    def rename_video(self):
        video_path = QtWidgets.QFileDialog.getOpenFileName(self, '打开图片', r'my_dataset/','Video Files(*.mp4)')
        if video_path != '':
            self.rename_video_line.setText(video_path)
            video_path = video_path.replace('\\', '\\\\')
            src_dir = os.path.dirname(video_path)
            file = os.path.basename(video_path)
            new_name = ''
            type = self.videoTypeCombo.currentText()
            if os.path.isfile(os.path.join(src_dir, file)) == True:
                if type == 'cars':
                    new_name = 'cars.mp4'
                elif type == 'people':
                    new_name = 'people.mp4'
                if file == new_name:
                    print('Name already in format.')
                else:
                    os.rename(os.path.join(src_dir, file), os.path.join(src_dir, new_name))
                    print(file, 'ok')

