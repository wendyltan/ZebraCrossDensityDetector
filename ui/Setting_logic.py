#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2019/3/14 16:41
# @Author  : wendy
# @Usage   : Dialog logic for setting
# @File    : Setting_logic.py
# @Software: PyCharm
from PyQt5 import QtWidgets
from ui.SettingDialog import Ui_Dialog

class SettingDialog(QtWidgets.QDialog,Ui_Dialog):
    def __init__(self):
        super(SettingDialog,self).__init__()
        self.setupUi(self)
        self.setWindowTitle('设置')
