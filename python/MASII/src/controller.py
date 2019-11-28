# -*- coding: utf-8 -*-
#######################################################
# main controller classes
#  - from src.controller import *
#  - example:
#     - 
#     - 
#######################################################
from ui.ui_mainwindow import *
from utils.common_funcs import *

import numpy as np
import traceback

import pyqtgraph as pg
import pyqtgraph.opengl as gl


import time
import serial
#import threading

class Controller(object):
    def __init__(self, main_window):
        '''
        init global setting
        '''
        self.main_window = main_window                
        
        #self.load_setting()
        
    def load_setting(self):        
        '''
        load global settings
        '''
        self.main_window.refresh()        
        return
       
    def message(self, msg=""):
        logging.info(msg)
        pass
   

    @unimplemented        
    def load_mesh(self, file_path):
        pass
    
    @unimplemented        
    def load_inp(self, file_path):
        pass    
        
    @unimplemented
    def save_config(self):        
        pass
        
    @unimplemented
    def any_init(self):
        try:
            pass
            
        except Exception as e:
            logging.info(traceback.format_exc())
        return    
    
    