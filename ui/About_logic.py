#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2019/3/14 15:45
# @Author  : wendy
# @Usage   : 
# @File    : About_logic.py
# @Software: PyCharm
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from utils import helper as hp
from ui.AboutDialog import Ui_Dialog
from utils import markdown_convertor as md
class AboutDialog(QtWidgets.QDialog,Ui_Dialog):
    def __init__(self):
        super(AboutDialog,self).__init__()
        self.setupUi(self)
        self.setFixedSize(501, 371)

        self.webView = QWebEngineView(self)
        self.webView.setGeometry(QtCore.QRect(0, 20, 481, 281))
        self.webView.setObjectName("webView")


        filenames = 'README'
        md.convert(filenames)
        path = hp.load_file(filenames+'.html')
        self.webView.load(QUrl.fromLocalFile(path))
        self.webView.show()
        self.setWindowTitle(filenames)

