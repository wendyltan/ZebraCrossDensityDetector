#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2019/3/14 16:41
# @Author  : wendy
# @Usage   : Dialog logic for setting
# @File    : Setting_logic.py
# @Software: PyCharm
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QWidget

from ui.SettingDialog import Ui_Dialog
from model.Config import Config as C
class SettingDialog(QtWidgets.QDialog,Ui_Dialog):
    def __init__(self):
        super(SettingDialog,self).__init__()
        self.conf = C()
        self.setupUi(self)
        self.setWindowTitle('设置')
        self.setFixedSize(610, 695)
        self.read_setting()
        self.confirmBtn.clicked.connect(self.confirm_setting)
        self.cancelBtn.clicked.connect(self.close)
        self.choose_result_path_btn.clicked.connect(self.choose_result_path)
        self.choose_result_html_btn.clicked.connect(self.choose_result_html)
        self.choose_result_text_btn.clicked.connect(self.choose_result_text)
        self.choose_video_path_btn.clicked.connect(self.choose_video_path)


    def read_setting(self):

        self.one_zebra.setText(self.conf.MAX_ALLOWED_DENSITY_ONE_ZEBRA)
        self.triangle_zebra.setText(self.conf.MAX_ALLOWED_DENSITY_TRIANGLE_ZEBRA)
        self.rectangle_zebra.setText(self.conf.MAX_ALLOWED_DENSITY_RECTANGLE_ZEBRA)

        self.person_weight.setText(self.conf.PERSON_WEIGHT)
        self.pet_weight.setText(self.conf.PET_WEIGHT)
        self.car_weight.setText(self.conf.CAR_WEIGHT)
        self.bike_weight.setText(self.conf.BIKE_WEIGHT)

        self.default_video_path.setText(self.conf.DEFAULT_VIDEO_PATH)
        self.default_result_path.setText(self.conf.DEFAULT_RESULT_PATH)
        self.default_result_text.setText(self.conf.PREDICT_RESULT_PATH)
        self.default_result_html.setText(self.conf.PREDICT_RESULT_IMAGE)

        self.max_image_num.setText(self.conf.MAX_SAVED_IMAGE)

    def confirm_setting(self):
        self.conf.set_config_file("global setting","default_video_path",
                                  self.default_video_path.text())
        self.conf.set_config_file("global setting","default_result_path",
                                    self.default_result_path.text())
        self.conf.set_config_file("global setting", "predict_result_image",
                                    self.default_result_html.text())
        self.conf.set_config_file("global setting", "predict_result_path",
                                    self.default_result_text.text())


        self.conf.set_config_file("weight setting", "person_weight",
                                    self.person_weight.text())
        self.conf.set_config_file("weight setting", "bike_weight",
                                    self.bike_weight.text())
        self.conf.set_config_file("weight setting", "pet_weight",
                                    self.pet_weight.text())
        self.conf.set_config_file("weight setting", "car_weight",
                                    self.car_weight.text())

        self.conf.set_config_file("max density setting", "max_allowed_density_one_zebra",
                                    self.one_zebra.text())
        self.conf.set_config_file("max density setting", "max_allowed_density_triangle_zebra",
                                    self.triangle_zebra.text())
        self.conf.set_config_file("max density setting", "max_allowed_density_rectangle_zebra",
                                    self.rectangle_zebra.text())

        self.conf.set_config_file("global setting","max_saved_image",
                                  self.max_image_num.text())


        reply = QMessageBox.information(QWidget(),'通知','是否确认按当前配置设置？',QMessageBox.Yes|QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.conf.write_config_file()
            ok = QMessageBox.information(QWidget(),'通知','设置成功！',QMessageBox.Yes)
            if ok == QMessageBox.Yes:
                self.close()
        else:
            # do nothing
            self.close()

    def choose_result_path(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(self,'选择路径',r'my_dataset/')
        if path != '':
            self.default_result_path.setText(path)

    def choose_result_html(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(self, '选择路径', r'my_dataset/')
        if path != '':
            self.default_result_html.setText(path)


    def choose_result_text(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(self, '选择路径', r'my_dataset/')
        if path != '':
            self.default_result_text.setText(path)

    def choose_video_path(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(self, '选择路径', r'my_dataset/')
        if path != '':
            self.default_video_path.setText(path)


