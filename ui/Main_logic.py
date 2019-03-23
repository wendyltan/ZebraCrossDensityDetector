#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2019/3/14 11:13
# @Author  : wendy
# @Usage   : Add or delete logic for main window here
# @File    : Main_logic.py
# @Software: PyCharm

import sys
import time
from turtledemo.nim import COLOR

from PyQt5 import QtWidgets
from PyQt5.QtCore import QUrl, QMutexLocker, QThread, pyqtSignal, QObject, QMutex, QTimer
from PyQt5.QtGui import QIcon, QImage, QPixmap
from PyQt5.QtWidgets import QGraphicsScene
from cv2 import cvtColor

import density_cal as dcl
from utils import helper as hp
from model.Zebra import Zebra
from ui.MainWindow import Ui_MainWindow
from ui.About_logic import AboutDialog
from config import Config as C
from ui.Setting_logic import SettingDialog
from PyQt5 import QtCore,QtGui
from PyQt5.QtWebEngineWidgets import *
import cv2

# init the config object
C = C()


class EmittingStream(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))


class MainWindow(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.setupUi(self)

        self.webView = QWebEngineView(self.resultArea)
        self.webView.setGeometry(QtCore.QRect(0, 20, 481, 281))
        self.webView.setObjectName("webView")
        self.webView.show()

        self.setWindowIcon(QIcon(C.ICON_PATH))
        self.statusBrowser.setReadOnly(True)


        self.actionabout.triggered.connect(self.about)
        self.actioncommon_setting.triggered.connect(self.setting)

        self.chooseModelCombo.addItems(['single','muti'])
        self.chooseZebraCombo.addItems(['one_zebra','tri_zebra','rec_zebra'])
        self.chooseVideoType.addItems(['video_file','camera'])

        self.detectButton.clicked.connect(self.start_detect)
        self.resetButton.clicked.connect(self.reset_default)

        self.mode = 'image'
        self.imageOptions.setEnabled(True)
        self.videoOptions.setEnabled(False)
        self.action_image_mode.changed.connect(self.mode_change)
        self.action_video_mode.changed.connect(self.mode_change)

        self.image_mode = 'single'
        self.singleImageCheckbox.setChecked(True)
        self.singleImageCheckbox.clicked.connect(self.image_mode_select)
        self.imageDirCheckbox.clicked.connect(self.image_mode_select)
        self.chooseImageBtn.clicked.connect(self.single_image)

        self.chooseVideoType.activated[str].connect(self.select_videoType)
        self.cap = cv2.VideoCapture()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showFrame)


        sys.stdout = EmittingStream(textWritten=self.normalOutputWritten)
        sys.stderr = EmittingStream(textWritten=self.normalOutputWritten)

    def showFrame(self):
        if self.cap.isOpened():
            ret,frame = self.cap.read()
            if ret:
                self.showImage(frame)
            else:
                self.cap.release()
                self.timer.stop()

    def showImage(self,src_img):
        src_img = cv2.cvtColor(src_img,cv2.COLOR_BGR2RGB)
        height,width,bytesPerComponent = src_img.shape
        bytesPerLine = bytesPerComponent * width
        q_image = QImage(src_img.data,width,height,bytesPerLine,QImage.Format_RGB888)
        img = q_image.scaled(self.graphicsView.width(), self.graphicsView.height())
        scene = QGraphicsScene()
        scene.addPixmap(QPixmap().fromImage(img))
        self.graphicsView.setScene(scene)


    def select_videoType(self):
        type = self.chooseVideoType.currentText()
        C.set_config_file("global setting","default_video_source",type)

    def single_image(self):
        # open one single image with file dialog and place it to the graphical view
        file_name,_ = QtWidgets.QFileDialog.getOpenFileName(self,'打开图片',r'my_dataset/', 'Image Files(*.jpg *.jpeg *.png)')
        self.imagePathLineEdit.setText(file_name)
        self.set_image_view(file_name)

    def set_image_view(self,file_name):
        img = QImage()
        img.load(file_name)
        img = img.scaled(self.graphicsView.width(), self.graphicsView.height())
        scene = QGraphicsScene()
        scene.addPixmap(QPixmap().fromImage(img))
        self.graphicsView.setScene(scene)

    def setting(self):
        setting_dialog = SettingDialog()
        setting_dialog.setWindowIcon(self.windowIcon())
        setting_dialog.show()
        setting_dialog.exec_()


    def about(self):
        about_dialog = AboutDialog()
        about_dialog.setWindowIcon(self.windowIcon())
        about_dialog.show()
        about_dialog.exec_()

    def do_detect(self,image_path):
        zebra = Zebra(self.chooseZebraCombo.currentText(), self.chooseModelCombo.currentText())
        print('Applying scene: ', zebra.get_name(), '.Using mode:', zebra.get_mode())
        dcl.zebra_cross(dcl.get_predictions(zebra, self.mode, image_path), zebra)

        latest_file_name = hp.get_latest_file(C.PREDICT_RESULT_IMAGE)
        file_path = hp.load_file((C.PREDICT_RESULT_IMAGE + latest_file_name).replace('/', '\\'))
        self.webView.load(QUrl.fromLocalFile(file_path))


    def start_detect(self):

        image_path = ''
        if self.mode == 'image' and self.image_mode == 'single':
            # only predict by one zebra when image is only single
            self.chooseZebraCombo.setCurrentIndex(0)
            image_path = self.imagePathLineEdit.text()
            self.do_detect(image_path)
            file_name = hp.get_latest_file(C.DEFAULT_RESULT_PATH+'/')
            file_path = hp.load_file(C.DEFAULT_RESULT_PATH+'/'+file_name)
            self.set_image_view(file_path)

        elif self.mode == 'image' and self.image_mode == 'directory':
            self.do_detect(image_path)
        elif self.mode == 'video':
            if self.chooseVideoType.currentText() == 'video_file':
                # open video dialog
                base_path = C.DEFAULT_VIDEO_PATH
                if self.chooseZebraCombo.currentText() == 'one_zebra':
                    path = base_path+'people.mp4'
                    self.cap.open(path)
                    self.timer.start(30)
                elif self.chooseZebraCombo.currentText() == 'tri_zebra' or\
                    self.chooseZebraCombo.currentText() == 'rec_zebra':

                    # not yet complete for playing two video one by one
                    path = base_path+'people.mp4'
                    self.cap.open(path)
                    self.timer.start(30)
                    path = base_path+'cars.mp4'
                    self.cap.open(path)
                    self.timer.start(30)

            elif self.chooseVideoType.currentText() == 'camera':
                pass
                # show camera
            self.do_detect(image_path)






    def reset_default(self):
        self.chooseModelCombo.setCurrentIndex(0)
        self.chooseZebraCombo.setCurrentIndex(0)
        self.chooseVideoType.setCurrentIndex(0)


    def __del__(self):
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    def normalOutputWritten(self, text):
        cursor = self.statusBrowser.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.statusBrowser.setTextCursor(cursor)
        self.statusBrowser.ensureCursorVisible()


    def mode_change(self):
        if self.mode == 'video' and self.action_video_mode.isChecked():
            self.action_image_mode.setChecked(True)
            self.action_video_mode.setChecked(False)
            self.mode = 'image'
            self.imageOptions.setEnabled(True)
            self.videoOptions.setEnabled(False)

        elif self.mode == 'image' and self.action_image_mode.isChecked():
            self.action_image_mode.setChecked(False)
            self.action_video_mode.setChecked(True)
            self.mode = 'video'
            self.videoOptions.setEnabled(True)
            self.imageOptions.setEnabled(False)



    def image_mode_select(self):
        if self.image_mode == 'single' and self.imageDirCheckbox.isChecked():
            self.singleImageCheckbox.setChecked(False)
            self.chooseImageBtn.setEnabled(False)
            self.image_mode = 'directory'
            self.imagePathLineEdit.setText('search under my_dataset/')
        elif self.image_mode == 'directory' and self.singleImageCheckbox.isChecked():
            self.imageDirCheckbox.setChecked(False)
            self.image_mode = 'single'
            self.chooseImageBtn.setEnabled(True)






