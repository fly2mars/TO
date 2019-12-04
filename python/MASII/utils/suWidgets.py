# -*- coding: utf-8 -*-
#######################################################
#       Widget class
#######################################################    
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QAction, QTableWidget, QTableWidgetItem, QHeaderView, QComboBox
from PyQt5.QtCore import pyqtSlot

class GCodeView(QTableWidget):
    def __init__(self, parent_widget=None):
        super(DictView, self).__init__(parent_widget)
        self.data = {}
        
        self.horizontalHeader().hide()
        self.verticalHeader().hide() 
        self.setAlternatingRowColors( True )
        #self.setRowCount(4)
        #self.setColumnCount(2)
        #self.setColumnWidth(10, 10)        
        
    
    def bind_data(self, file_name):
        if dict_data is None:
            dict_data = self.data
        else:
            self.data = dict_data
        
        self.setRowCount(len(dict_data))
        self.setColumnCount(2)
        self.setColumnWidth(0, 120)
        self.setColumnWidth(1, 198)
        #self.setRowHeight(5,5)        
        i = 0
        for key, value in dict_data.items():
            self.setItem(i, 0, QTableWidgetItem(key))
            self.setItem(i, 1, QTableWidgetItem(str(value)))
            i += 1
        #self.move(0 , 0)        
        
    def get_value(self):
        model = self.model()
        self.data = {}
        for row in range(model.rowCount()):
            index = model.index(row, 0)
            key = str(model.data(index).toString())
            index = model.index(row, 1)
            value = model.data(index)
            self.data[key] = value   
            
        return self.data
        
    def set_value(self, key, value):
        self.data[key] = value
        self.bind_data(self.data)
        
class DictView(QTableWidget):
    def __init__(self, parent_widget=None):
        super(DictView, self).__init__(parent_widget)
        self.data = {}
        
        self.horizontalHeader().hide()
        self.verticalHeader().hide() 
        self.setAlternatingRowColors( True )
        #self.setRowCount(4)
        #self.setColumnCount(2)
        #self.setColumnWidth(10, 10)        
        
    
    def bind_data(self, dict_data=None):
        if dict_data is None:
            dict_data = self.data
        else:
            self.data = dict_data
        
        self.setRowCount(len(dict_data))
        self.setColumnCount(2)
        self.setColumnWidth(0, 120)
        self.setColumnWidth(1, 198)
        #self.setRowHeight(5,5)        
        i = 0
        for key, value in dict_data.items():
            self.setItem(i, 0, QTableWidgetItem(key))
            self.setItem(i, 1, QTableWidgetItem(str(value)))
            i += 1
        #self.move(0 , 0)        
        
    def get_value(self):
        model = self.model()
        self.data = {}
        for row in range(model.rowCount()):
            index = model.index(row, 0)
            key = str(model.data(index).toString())
            index = model.index(row, 1)
            value = model.data(index)
            self.data[key] = value   
            
        return self.data
        
    def set_value(self, key, value):
        self.data[key] = value
        self.bind_data(self.data)
        
        
class ComboAddress(QComboBox):
    def __init__(self,parent_widget):
        super(ComboAddress, self).__init__(parent_widget)
    # add address from config
    def add_address(self, dict_data):
        for k, v in dict_data.items():
            if k=='地址':
                self.addItem(str(v))
                
    def get_curent_select(self):
        return str(self.currentText())
    