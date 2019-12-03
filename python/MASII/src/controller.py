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
from utils.beso_lib import *

import numpy as np
import traceback

import pyqtgraph as pg
import pyqtgraph.opengl as gl


import time
import serial
#import threading
import utils.beso_lib

class VolumeModel(object):
    def __init__(self):
        self.nodes = None
        self.elements = None
        self.constraint_nodes = None  # node index
        self.load_nodes = None        # node index
        self.elset_name = "SolidMaterialElementGeometry2D"   # string with name of the element set in .inp file
        
        
    def load(self, file_path):
        domain_optimized = {}   
        domain_optimized[self.elset_name] = True  # True - optimized domain, False - elements will not be removed
        domains_from_config = domain_optimized.keys()    
        shells_as_composite = False  # True - use more integration points to catch bending stresses (ccx 2.12 WILL FAIL for other than S8R and S6 shell elements)
                                     # False - use ordinary shell section                
        [self.nodes, self.Elements, self.domains, self.opt_domains, en_all,
         plane_strain, plane_stress, axisymmetry] = utils.beso_lib.import_inp(
             file_path, domains_from_config, domain_optimized, shells_as_composite)
        
        self.load_nodes = list(np.array(list(utils.beso_lib.import_inp_load(file_path).keys())) - 1)  # index from 1 to 0 
        self.constraint_nodes = list(np.array(utils.beso_lib.import_inp_boundary(file_path)) - 1)     # index from 1 to 0
        
    def get_nodes(self):
        nodes = []
        if self.nodes is not None:
            return np.array(list(self.nodes.values()))
            
        
    def bbox(self):
        bbox = np.zeros([2,3])
        if self.nodes is not None:
            nodes = np.array(list(self.nodes.values()))
            bbox[0] = np.min(nodes,0)
            bbox[1] = np.max(nodes,0)
            
        return bbox
        
        
               

class Controller(object):
    def __init__(self, main_window):
        '''
        init global setting
        '''
        self.main_window = main_window
        self.volume_model = VolumeModel()
        
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
              
    def load_inp(self, file_path):
        self.volume_model.load(file_path)                 
        self.show_model()
        pass
    
    @unimplemented
    def show_model(self):   
        nodes = self.volume_model.get_nodes()
        size = nodes.shape[0]
        colors = np.zeros((size, 4))
        colors[:,3] = 0.9
        colors[:,0] = 1.0
        
        colors[self.volume_model.constraint_nodes] = [1,1,1,0.9]
        colors[self.volume_model.load_nodes] = [1,1,0,0.9]
        nds = gl.GLScatterPlotItem(pos=nodes, color = colors, size=0.9, pxMode = False)
        
        self.main_window.model_view.addItem(nds)        
        self.main_window.repaint()    
        
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
    
    