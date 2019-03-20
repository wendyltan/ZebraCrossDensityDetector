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
from model.Zebra import Zebra
from ui.MainWindow import Ui_MainWindow
from  ui.About_logic import AboutDialog
from config import Config as C
from ui.Setting_logic import SettingDialog
from PyQt5 import QtCore,QtGui
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
        self.actionopen_singe_image.triggered.connect(self.single_image)
        self.actioncommon_setting.triggered.connect(self.setting)

        self.chooseModelCombo.addItems(['single','muti'])
        self.chooseZebraCombo.addItems(['one_zebra','tri_zebra','rec_zebra'])
        self.chooseVideoType.addItems(['video_file','camera'])

        self.detectButton.clicked.connect(self.start_detect)
        self.resetButton.clicked.connect(self.reset_default)

        sys.stdout = EmittingStream(textWritten=self.normalOutputWritten)
        sys.stderr = EmittingStream(textWritten=self.normalOutputWritten)



    def single_image(self):
        # open one single image with file dialog and place it to the graphical view
        file_name,_= QtWidgets.QFileDialog.getOpenFileName(self,'打开图片',r'my_dataset/', 'Image Files(*.jpg *.jpeg *.png)')
        img = QImage()
        img.load(file_name)
        img = img.scaled(self.graphicsView.width(),self.graphicsView.height())
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


    def start_detect(self):
        zebra = Zebra(self.chooseZebraCombo.currentText(), self.chooseModelCombo.currentText())
        print('Applying scene: ', zebra.get_name(), '.Using mode:', zebra.get_mode())
        dcl.zebra_cross(dcl.get_predictions(zebra, 'image'), zebra)

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




