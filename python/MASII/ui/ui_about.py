# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'about.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AboutDialog(object):
    def setupUi(self, AboutDialog):
        AboutDialog.setObjectName("AboutDialog")
        AboutDialog.resize(400, 300)
        self.label = QtWidgets.QLabel(AboutDialog)
        self.label.setGeometry(QtCore.QRect(60, 60, 321, 41))
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(AboutDialog)
        self.label_2.setGeometry(QtCore.QRect(140, 130, 101, 41))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(AboutDialog)
        self.label_3.setGeometry(QtCore.QRect(100, 160, 201, 41))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(AboutDialog)
        self.label_4.setGeometry(QtCore.QRect(90, 200, 221, 41))
        self.label_4.setObjectName("label_4")
        self.cb_OK = QtWidgets.QPushButton(AboutDialog)
        self.cb_OK.setGeometry(QtCore.QRect(280, 260, 93, 28))
        self.cb_OK.setObjectName("cb_OK")

        self.retranslateUi(AboutDialog)
        self.cb_OK.clicked.connect(AboutDialog.close)
        QtCore.QMetaObject.connectSlotsByName(AboutDialog)

    def retranslateUi(self, AboutDialog):
        _translate = QtCore.QCoreApplication.translate
        AboutDialog.setWindowTitle(_translate("AboutDialog", "关于"))
        self.label.setText(_translate("AboutDialog", "多轴长纤增强打印系统"))
        self.label_2.setText(_translate("AboutDialog", "Version 1.0"))
        self.label_3.setText(_translate("AboutDialog", "上海大学快速制造工程中心"))
        self.label_4.setText(_translate("AboutDialog", "<a href=\"http://www.rmec.shu.edu.cn\">http://www.rmec.shu.edu.cn</a>"))
        self.cb_OK.setText(_translate("AboutDialog", "确定"))

import resource_rc
