# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1335, 859)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icon.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.text_console = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.text_console.setGeometry(QtCore.QRect(680, 700, 641, 101))
        self.text_console.setObjectName("text_console")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 430, 651, 321))
        self.groupBox.setObjectName("groupBox")
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_2.setGeometry(QtCore.QRect(414, 284, 93, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_4 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_4.setGeometry(QtCore.QRect(521, 284, 93, 28))
        self.pushButton_4.setObjectName("pushButton_4")
        self.textBrowser_rule = QtWidgets.QTextBrowser(self.groupBox)
        self.textBrowser_rule.setGeometry(QtCore.QRect(300, 70, 341, 201))
        self.textBrowser_rule.setObjectName("textBrowser_rule")
        self.pushButton_5 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_5.setGeometry(QtCore.QRect(370, 30, 118, 28))
        self.pushButton_5.setObjectName("pushButton_5")
        self.comboBox_4 = QtWidgets.QComboBox(self.groupBox)
        self.comboBox_4.setGeometry(QtCore.QRect(300, 289, 101, 22))
        self.comboBox_4.setObjectName("comboBox_4")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.pushButton_15 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_15.setGeometry(QtCore.QRect(510, 30, 127, 28))
        self.pushButton_15.setObjectName("pushButton_15")
        self.comboBox_11 = QtWidgets.QComboBox(self.groupBox)
        self.comboBox_11.setGeometry(QtCore.QRect(303, 32, 51, 22))
        self.comboBox_11.setObjectName("comboBox_11")
        self.comboBox_11.addItem("")
        self.comboBox_11.addItem("")
        self.comboBox_11.addItem("")
        self.comboBox_5 = QtWidgets.QComboBox(self.groupBox)
        self.comboBox_5.setGeometry(QtCore.QRect(80, 30, 196, 22))
        self.comboBox_5.setObjectName("comboBox_5")
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(11, 34, 72, 15))
        self.label_2.setObjectName("label_2")
        self.dview_rules = DictView(self.groupBox)
        self.dview_rules.setGeometry(QtCore.QRect(10, 60, 271, 251))
        self.dview_rules.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.dview_rules.setObjectName("dview_rules")
        self.dview_rules.setColumnCount(0)
        self.dview_rules.setRowCount(0)
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 10, 651, 231))
        self.groupBox_3.setObjectName("groupBox_3")
        self.pushButton = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton.setGeometry(QtCore.QRect(300, 190, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_3 = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_3.setGeometry(QtCore.QRect(410, 190, 93, 28))
        self.pushButton_3.setObjectName("pushButton_3")
        self.comb_variable_to_fact_func = QtWidgets.QComboBox(self.groupBox_3)
        self.comb_variable_to_fact_func.setGeometry(QtCore.QRect(450, 160, 121, 22))
        self.comb_variable_to_fact_func.setObjectName("comb_variable_to_fact_func")
        self.line_edit_state = QtWidgets.QLineEdit(self.groupBox_3)
        self.line_edit_state.setEnabled(False)
        self.line_edit_state.setGeometry(QtCore.QRect(300, 160, 131, 21))
        self.line_edit_state.setObjectName("line_edit_state")
        self.line_edit_state_value = QtWidgets.QLineEdit(self.groupBox_3)
        self.line_edit_state_value.setGeometry(QtCore.QRect(590, 160, 51, 21))
        self.line_edit_state_value.setObjectName("line_edit_state_value")
        self.label = QtWidgets.QLabel(self.groupBox_3)
        self.label.setGeometry(QtCore.QRect(300, 20, 72, 15))
        self.label.setObjectName("label")
        self.dview_variables = DictView(self.groupBox_3)
        self.dview_variables.setEnabled(True)
        self.dview_variables.setGeometry(QtCore.QRect(300, 40, 341, 101))
        self.dview_variables.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.dview_variables.setObjectName("dview_variables")
        self.dview_variables.setColumnCount(0)
        self.dview_variables.setRowCount(0)
        self.dview_facts = DictView(self.groupBox_3)
        self.dview_facts.setGeometry(QtCore.QRect(10, 20, 271, 201))
        self.dview_facts.setObjectName("dview_facts")
        self.dview_facts.setColumnCount(0)
        self.dview_facts.setRowCount(0)
        self.pb_start = QtWidgets.QPushButton(self.centralwidget)
        self.pb_start.setEnabled(False)
        self.pb_start.setGeometry(QtCore.QRect(40, 760, 101, 41))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/imgs/imgs/start.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pb_start.setIcon(icon1)
        self.pb_start.setIconSize(QtCore.QSize(30, 30))
        self.pb_start.setObjectName("pb_start")
        self.pb_pause = QtWidgets.QPushButton(self.centralwidget)
        self.pb_pause.setEnabled(False)
        self.pb_pause.setGeometry(QtCore.QRect(160, 760, 101, 41))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/imgs/imgs/pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pb_pause.setIcon(icon2)
        self.pb_pause.setIconSize(QtCore.QSize(30, 30))
        self.pb_pause.setObjectName("pb_pause")
        self.pb_stop = QtWidgets.QPushButton(self.centralwidget)
        self.pb_stop.setEnabled(False)
        self.pb_stop.setGeometry(QtCore.QRect(290, 760, 101, 41))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/imgs/imgs/stop.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pb_stop.setIcon(icon3)
        self.pb_stop.setIconSize(QtCore.QSize(30, 30))
        self.pb_stop.setObjectName("pb_stop")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 240, 651, 181))
        self.groupBox_2.setObjectName("groupBox_2")
        self.pushButton_17 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_17.setGeometry(QtCore.QRect(300, 147, 93, 28))
        self.pushButton_17.setObjectName("pushButton_17")
        self.pushButton_18 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_18.setGeometry(QtCore.QRect(410, 147, 93, 28))
        self.pushButton_18.setObjectName("pushButton_18")
        self.dview_acts = DictView(self.groupBox_2)
        self.dview_acts.setGeometry(QtCore.QRect(10, 20, 271, 151))
        self.dview_acts.setObjectName("dview_acts")
        self.dview_acts.setColumnCount(0)
        self.dview_acts.setRowCount(0)
        self.textBrowser_act = QtWidgets.QTextBrowser(self.groupBox_2)
        self.textBrowser_act.setGeometry(QtCore.QRect(300, 10, 341, 131))
        self.textBrowser_act.setObjectName("textBrowser_act")
        self.groupBox_4 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_4.setGeometry(QtCore.QRect(680, 10, 641, 511))
        self.groupBox_4.setObjectName("groupBox_4")
        self.model_view = GLViewWidget(self.groupBox_4)
        self.model_view.setGeometry(QtCore.QRect(10, 30, 621, 461))
        self.model_view.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.model_view.setObjectName("model_view")
        self.groupBox_5 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_5.setGeometry(QtCore.QRect(680, 530, 641, 161))
        self.groupBox_5.setObjectName("groupBox_5")
        self.openGLWidget = QtWidgets.QOpenGLWidget(self.groupBox_5)
        self.openGLWidget.setGeometry(QtCore.QRect(10, 20, 621, 121))
        self.openGLWidget.setObjectName("openGLWidget")
        self.groupBox_2.raise_()
        self.groupBox.raise_()
        self.text_console.raise_()
        self.groupBox_3.raise_()
        self.pb_start.raise_()
        self.pb_pause.raise_()
        self.pb_stop.raise_()
        self.groupBox_4.raise_()
        self.groupBox_5.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1335, 26))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_about = QtWidgets.QMenu(self.menubar)
        self.menu_about.setObjectName("menu_about")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        self.menu_3 = QtWidgets.QMenu(self.menubar)
        self.menu_3.setObjectName("menu_3")
        MainWindow.setMenuBar(self.menubar)
        self.action_open = QtWidgets.QAction(MainWindow)
        self.action_open.setObjectName("action_open")
        self.action_exit = QtWidgets.QAction(MainWindow)
        self.action_exit.setObjectName("action_exit")
        self.action_about = QtWidgets.QAction(MainWindow)
        self.action_about.setObjectName("action_about")
        self.action_re_setting = QtWidgets.QAction(MainWindow)
        self.action_re_setting.setObjectName("action_re_setting")
        self.action_rule_load = QtWidgets.QAction(MainWindow)
        self.action_rule_load.setObjectName("action_rule_load")
        self.menu.addAction(self.action_open)
        self.menu.addSeparator()
        self.menu.addAction(self.action_exit)
        self.menu_about.addAction(self.action_about)
        self.menu_2.addAction(self.action_re_setting)
        self.menu_2.addAction(self.action_rule_load)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())
        self.menubar.addAction(self.menu_about.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "RMEC RDesigner"))
        self.groupBox.setTitle(_translate("MainWindow", "规则"))
        self.pushButton_2.setText(_translate("MainWindow", "添加"))
        self.pushButton_4.setText(_translate("MainWindow", "删除"))
        self.pushButton_5.setText(_translate("MainWindow", "+事实"))
        self.comboBox_4.setItemText(0, _translate("MainWindow", "硬性规则"))
        self.comboBox_4.setItemText(1, _translate("MainWindow", "可废止规则"))
        self.comboBox_4.setItemText(2, _translate("MainWindow", "废止者"))
        self.pushButton_15.setText(_translate("MainWindow", "+动作"))
        self.comboBox_11.setItemText(0, _translate("MainWindow", "与"))
        self.comboBox_11.setItemText(1, _translate("MainWindow", "或"))
        self.comboBox_11.setItemText(2, _translate("MainWindow", "非"))
        self.comboBox_5.setItemText(0, _translate("MainWindow", "硬性规则"))
        self.comboBox_5.setItemText(1, _translate("MainWindow", "可废止规则"))
        self.comboBox_5.setItemText(2, _translate("MainWindow", "废止者"))
        self.label_2.setText(_translate("MainWindow", "规则库："))
        self.groupBox_3.setTitle(_translate("MainWindow", "事实"))
        self.pushButton.setText(_translate("MainWindow", "添加"))
        self.pushButton_3.setText(_translate("MainWindow", "删除"))
        self.label.setText(_translate("MainWindow", "环境变量"))
        self.pb_start.setText(_translate("MainWindow", "优化"))
        self.pb_pause.setText(_translate("MainWindow", "暂停"))
        self.pb_stop.setText(_translate("MainWindow", "停止"))
        self.groupBox_2.setTitle(_translate("MainWindow", "动作"))
        self.pushButton_17.setText(_translate("MainWindow", "添加"))
        self.pushButton_18.setText(_translate("MainWindow", "删除"))
        self.groupBox_4.setTitle(_translate("MainWindow", "模型"))
        self.groupBox_5.setTitle(_translate("MainWindow", "状态"))
        self.menu.setTitle(_translate("MainWindow", "文件"))
        self.menu_about.setTitle(_translate("MainWindow", "关于"))
        self.menu_2.setTitle(_translate("MainWindow", "引擎"))
        self.menu_3.setTitle(_translate("MainWindow", "视图"))
        self.action_open.setText(_translate("MainWindow", "打开.."))
        self.action_exit.setText(_translate("MainWindow", "退出"))
        self.action_about.setText(_translate("MainWindow", "关于"))
        self.action_re_setting.setText(_translate("MainWindow", "引擎设置..."))
        self.action_rule_load.setText(_translate("MainWindow", "装入规则..."))

from pyqtgraph.opengl.GLViewWidget import GLViewWidget
from utils.suWidgets import DictView
import resource_rc
