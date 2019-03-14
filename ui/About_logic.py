#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2019/3/14 15:45
# @Author  : wendy
# @Usage   : 
# @File    : About_logic.py
# @Software: PyCharm
from PyQt5 import QtWidgets
from ui.AboutDialog import Ui_Dialog

class AboutDialog(QtWidgets.QDialog,Ui_Dialog):
    def __init__(self):
        super(AboutDialog,self).__init__()
        self.setupUi(self)
        # the about content
        filenames = 'README.md'
        f = open(filenames, 'r')
        self.textBrowser.setText(f.read())
        self.setWindowTitle(filenames)
