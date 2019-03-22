#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2019/3/14 11:13
# @Author  : wendy
# @Usage   : Add or delete logic for main window here
# @File    : Main_logic.py
# @Software: PyCharm
import os
import sys

from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon, QImage, QPixmap
from PyQt5.QtWidgets import QGraphicsScene

import density_cal as dcl
import predictor as pd

from model.Zebra import Zebra
from ui.MainWindow import Ui_MainWindow
from  ui.About_logic import AboutDialog
from config import Config as C
from ui.Setting_logic import SettingDialog
from PyQt5 import QtCore,QtGui

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
        self.setWindowIcon(QIcon(C.ICON_PATH))

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
        self.chooseDirBtn.setEnabled(False)
        self.singleImageCheckbox.clicked.connect(self.image_mode_select)
        self.imageDirCheckbox.clicked.connect(self.image_mode_select)

        self.chooseImageBtn.clicked.connect(self.single_image)
        self.chooseDirBtn.clicked.connect(self.image_dir)


        sys.stdout = EmittingStream(textWritten=self.normalOutputWritten)
        sys.stderr = EmittingStream(textWritten=self.normalOutputWritten)



    def single_image(self):
        # open one single image with file dialog and place it to the graphical view
        file_name,_ = QtWidgets.QFileDialog.getOpenFileName(self,'打开图片',r'my_dataset/', 'Image Files(*.jpg *.jpeg *.png)')
        self.imagePathLineEdit.setText(file_name)
        img = QImage()
        img.load(file_name)
        img = img.scaled(self.graphicsView.width(),self.graphicsView.height())
        scene = QGraphicsScene()
        scene.addPixmap(QPixmap().fromImage(img))
        self.graphicsView.setScene(scene)

    def image_dir(self):
        file_path = QtWidgets.QFileDialog.getExistingDirectory(self,'选择图片文件夹',r'my_dataset/')
        self.imagePathLineEdit.setText(file_path)


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


    def start_detect(self):
        if self.mode == 'image' and self.image_mode == 'single':
            # only predict by one zebra when image is only single
            self.chooseZebraCombo.setCurrentIndex(0)
            zebra = Zebra(self.chooseZebraCombo.currentText(),self.chooseModelCombo.currentText())
            image_path = self.imagePathLineEdit.text()
            # image_path = r'my_dataset\zebra_people\4.jpg'
            print('Applying scene: ', zebra.get_name(), '.Using mode:', zebra.get_mode())
            dcl.zebra_cross(dcl.get_predictions(zebra, self.mode, image_path), zebra)



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
            self.chooseDirBtn.setEnabled(True)
        elif self.image_mode == 'directory' and self.singleImageCheckbox.isChecked():
            self.imageDirCheckbox.setChecked(False)
            self.chooseDirBtn.setEnabled(False)
            self.image_mode = 'single'
            self.chooseImageBtn.setEnabled(True)








