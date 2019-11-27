# -*- coding: utf-8 -*-
############## View class for main_window########
#  - 包含主要的界面控制函数
#  - 功能性函数在controller类中实现
#################################################
import time
from ui.ui_mainwindow import *
from ui.ui_about import *
from utils.class_base import *
from PyQt5.QtWidgets import QWidget, QDialog, QFileDialog, QSplashScreen
from PyQt5.QtGui import(QFont, QIcon, QImage, QPixmap) 
from PyQt5.QtCore import QBasicTimer

from os import path
from src.controller import Controller

class Viewer(Ui_MainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()     
        splash_pix = QPixmap(':/imgs/imgs/splash.png')
        self.splash = QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
        self.splash.show()         
                
        self.controller = Controller(self)   
        self.progress = 0
        self.timer = QBasicTimer()
        
        
        
    
    def setupUi(self, MainWindow):
        self.MainWindow = MainWindow
        Ui_MainWindow.setupUi(self,MainWindow)                            
     
        self.load_config()    
        
        # set logger window
        self.logger = WinLogger(self.text_console)
        self.logger.register_logger()            
        self._connect_signals(MainWindow)
        self.setFixedSize(self.size())
        self.splash.close()  
        
    def _connect_signals(self, MainWindow):
        # menu action        
        self.action_exit.triggered.connect(self.app_quit)
        self.action_about.triggered.connect(self.about)        
        
        # button action        
        #self.pb_start.clicked.connect(self.b_start)
        #self.pb_stop.clicked.connect(self.b_stop)
        #self.pb_pause.clicked.connect(self.b_pause)   
 
 # Menu actions       
    def app_quit(self):
        self.MainWindow.close()
    
    def about(self):
        dialog = QDialog()
        dialog.ui = Ui_AboutDialog()
        dialog.ui.setupUi(dialog)
        dialog.setModal(True)
        dialog.show()
        dialog.exec_()
   
    def load_config(self):
        #self.controller.load_setting()            
        #self.refresh()
        return
    
    def load_file(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '', 
                                            "mesh model (*.stl);; volume data (*.inp);")
        for s in fname:
            logging.debug(s)
        if fname[0]:
            ext_file = path.splitext(fname[0])[1]
            if  ext_file in fname[1]:                
                logging.info("Load " + fname[0])
                if ext_file == '.path':
                    self.controller.load_model(fname[0])
            else:
                return        
       
    