#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2019/3/14 11:13
# @Author  : wendy
# @Usage   : Add or delete logic for main window here
# @File    : Main_logic.py
# @Software: PyCharm
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon, QImage, QPixmap
from PyQt5.QtWidgets import QGraphicsScene

from ui.MainWindow import Ui_MainWindow
from  ui.About_logic import AboutDialog
import config as C
from ui.Setting_logic import SettingDialog


class MainWindow(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(C.ICON_PATH))

        self.actionabout.triggered.connect(self.about)
        self.actionopen_singe_image.triggered.connect(self.single_image)
        self.actioncommon_setting.triggered.connect(self.setting)


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

