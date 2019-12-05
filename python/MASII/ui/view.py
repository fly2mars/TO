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
from src.sufact import FactOperator

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
     
        # set logger window
        self.logger = WinLogger(self.text_console)
        self.logger.register_logger()            
        self._connect_signals(MainWindow)
        self.setFixedSize(self.size())
        
        self.load_config()   
        self.splash.close()  
        
    def _connect_signals(self, MainWindow):
        # menu action        
        self.action_exit.triggered.connect(self.app_quit)
        self.action_open.triggered.connect(self.load_file)
        self.action_about.triggered.connect(self.about)      
        
        self.dview_variables.cellClicked.connect(self.controller.update_cur_fact)
        
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
        
        #init view
        ## init fact operators
        fo = FactOperator()
        operators = fo.get_operators()
        self.comb_variable_to_fact_func.addItems(operators)
            
        return
    
    def load_file(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '', 
                                            "volume data (*.inp);; mesh model (*.stl);")
        for s in fname:
            logging.debug(s)
        if fname[0]:
            ext_file = path.splitext(fname[0])[1]
            if  ext_file in fname[1]:                
                logging.info("Load " + fname[0])
                if ext_file == '.stl':
                    self.controller.load_mesh(fname[0])
                if ext_file == '.inp':
                    self.controller.load_inp(fname[0])
            else:
                return        
       
    