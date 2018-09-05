#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 26 21:05:17 2018

@author: jkevangelio
"""


import sys
from pprint import pprint
from PyQt5 import QtWidgets, QtGui, QtCore, Qt
from PyQt5.QtWidgets import QGridLayout,QLabel, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QMainWindow, QAction, qApp, QApplication
from PyQt5.QtGui import QIcon

import subprocess
import shlex
import threading
import time

class MainWindow(QMainWindow):
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        super().__init__()

        self.initWindow()
        
    def initWindow(self):
        self.setWindowTitle("WhiteShark")
        self.statusBar().showMessage("This is a status bar")
        self.setGeometry(200,100,1000,500)
        

        self.toolbar = self.addToolBar("Save")

        capture_action = QAction(QIcon("images/capture.png"), "&Capture", self)
        capture_action.setShortcut("Ctrl+C")
        capture_action.setStatusTip("Capture")
        capture_action.triggered.connect(self.createtable)

        stop_action = QAction(QIcon("images/stop.png"), "&Stop", self)
        stop_action.setShortcut("Ctrl+S")
        stop_action.setStatusTip("Stop")

        exit_action = QAction(QIcon("images/exit.png"), "&Exit", self)
        exit_action.setShortcut("Ctrl+q")
        exit_action.setStatusTip("Exit program")
        exit_action.triggered.connect(qApp.quit)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(capture_action)
        fileMenu.addAction(stop_action)
        fileMenu.addAction(exit_action)

        self.toolbar.addAction(capture_action)
        self.toolbar.addAction(stop_action)
        self.toolbar.addAction(exit_action)

       
        
        
        self.show()
        sys.exit(self.app.exec_())


    def createtable(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        grid_layout = QGridLayout(self)
        central_widget.setLayout(grid_layout)

        tableWidget = QTableWidget(self)
        tableWidget.setColumnCount(6)
        #tableWidget.setRowCount(1)
        tableWidget.setHorizontalHeaderLabels(["No","Time","Source","Destination","Protocol","Info"])
 
        # Fill the first line
        f = open("../tcpdump.txt","r")
        lines = [line for line in f if line.strip()]
        f.close()
        time=[]
        source=[]
        destination=[]
        protocol=[]
        info=[]

        for t in lines:
            time.append(t[:8])
    
        for s in lines:
            source.append(s[s.find("IP")+3:s.find(">")])
            
        for d in lines:
            destination.append(d[d.find(">")+2:d.find(":",d.find(">"))]) 

        for p in lines:
            initial = p.find(":",p.find(">"))+2
            rangee = p.find(" ", (initial))
            protocol.append(p[initial:p.find(" ", rangee)])

        for i in lines:
            initial = i.find(":",i.find(">"))+2
            info.append(i[initial:])
        
        #tableWidget.setRowCount(len(lines))
        time.reverse()
        source.reverse()
        destination.reverse()
        protocol.reverse()
        info.reverse()
        
        
        
        
        
        
        #for column, data in enumerate(lists):
#        for t,s,d,p,i in zip(time,source,destination,protocol,info):
#        for row in range(len(lines)):
        

        
        tableWidget.setRowCount(len(lines))
        for row in range(len(lines)):
            tableWidget.setItem(row,0, QTableWidgetItem(str(time[row])))
            tableWidget.setItem(row,1, QTableWidgetItem(str(source[row])))
            tableWidget.setItem(row,2, QTableWidgetItem(str(destination[row])))
            tableWidget.setItem(row,3, QTableWidgetItem(str(protocol[row])))
            tableWidget.setItem(row,4, QTableWidgetItem(str(info[row])))
            time.sleep(1)


        #tableWidget.setGeometry(5,60,990,450)

        header = tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        for column in range(1, 4):
            header.setSectionResizeMode(column, QtWidgets.QHeaderView.ResizeToContents)
            
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.Stretch)
        #tableWidget.resizeColumnsToContents()
        grid_layout.addWidget(tableWidget,0,0)
       



main = MainWindow()