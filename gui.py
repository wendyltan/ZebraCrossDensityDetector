#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2019/3/10 14:56
# @Author  : wendy
# @Usage   : Run the main gui of the user interface of the program.
# @File    : gui.py
# @Software: PyCharm
import sys
from ui.Main_logic import MainWindow
from PyQt5 import QtWidgets

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

