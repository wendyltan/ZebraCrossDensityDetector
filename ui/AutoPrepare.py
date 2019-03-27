# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AutoPrepare.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(639, 592)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 20, 81, 16))
        self.label.setObjectName("label")
        self.rename_images_line = QtWidgets.QLineEdit(Dialog)
        self.rename_images_line.setGeometry(QtCore.QRect(240, 20, 251, 21))
        self.rename_images_line.setObjectName("rename_images_line")
        self.chooseImageDir = QtWidgets.QPushButton(Dialog)
        self.chooseImageDir.setGeometry(QtCore.QRect(520, 20, 93, 28))
        self.chooseImageDir.setObjectName("chooseImageDir")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 60, 72, 15))
        self.label_2.setObjectName("label_2")
        self.fileTypeCombo = QtWidgets.QComboBox(Dialog)
        self.fileTypeCombo.setGeometry(QtCore.QRect(140, 60, 81, 22))
        self.fileTypeCombo.setCurrentText("")
        self.fileTypeCombo.setObjectName("fileTypeCombo")
        self.copy_file_line = QtWidgets.QLineEdit(Dialog)
        self.copy_file_line.setGeometry(QtCore.QRect(280, 60, 211, 21))
        self.copy_file_line.setObjectName("copy_file_line")
        self.chooseFile = QtWidgets.QPushButton(Dialog)
        self.chooseFile.setGeometry(QtCore.QRect(520, 60, 93, 28))
        self.chooseFile.setObjectName("chooseFile")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(20, 110, 111, 16))
        self.label_3.setObjectName("label_3")
        self.rename_video_line = QtWidgets.QLineEdit(Dialog)
        self.rename_video_line.setGeometry(QtCore.QRect(240, 110, 251, 21))
        self.rename_video_line.setObjectName("rename_video_line")
        self.chooseVideo = QtWidgets.QPushButton(Dialog)
        self.chooseVideo.setGeometry(QtCore.QRect(510, 110, 101, 28))
        self.chooseVideo.setObjectName("chooseVideo")
        self.dirTreeView = QtWidgets.QTreeView(Dialog)
        self.dirTreeView.setGeometry(QtCore.QRect(20, 160, 601, 421))
        self.dirTreeView.setObjectName("dirTreeView")
        self.videoTypeCombo = QtWidgets.QComboBox(Dialog)
        self.videoTypeCombo.setGeometry(QtCore.QRect(140, 110, 81, 22))
        self.videoTypeCombo.setCurrentText("")
        self.videoTypeCombo.setObjectName("videoTypeCombo")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "重命名图片"))
        self.chooseImageDir.setText(_translate("Dialog", "选择文件夹"))
        self.label_2.setText(_translate("Dialog", "拷贝文件"))
        self.chooseFile.setText(_translate("Dialog", "选择文件夹"))
        self.label_3.setText(_translate("Dialog", "重命名视频文件"))
        self.chooseVideo.setText(_translate("Dialog", "选择视频文件"))


