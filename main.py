import sys
from pprint import pprint
from PyQt5 import QtWidgets, QtGui, QtCore, Qt
from PyQt5.QtWidgets import QGridLayout,QLabel, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QMainWindow, QAction, qApp, QApplication
from PyQt5.QtGui import QIcon

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
        capture_action.triggered.connect(self.insertitem)

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

       
        
        self.createtable()
        
        self.show()
        sys.exit(self.app.exec_())


    def createtable(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        grid_layout = QGridLayout(self)
        central_widget.setLayout(grid_layout)

        self.tableWidget = QTableWidget(self)
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderLabels(["No","Time","Source","Destination","Protocol","Info"])
 
        # Fill the first line
              


        #tableWidget.setGeometry(5,60,990,450)

        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        for i in range(1,5):
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
        
        #tableWidget.resizeColumnsToContents()
        grid_layout.addWidget(self.tableWidget,0,0)
        
    def insertitem(self):
        lists=[]
        self.loop = QtCore.QEventLoop(self)
        with open("testfile.txt") as f:
            for line in f:
                lists.append(line[0:5])
        numrows=[]
        for i in range(len(lists)):
            numrows.append(self.tableWidget.rowCount())
            self.tableWidget.insertRow(numrows[i])
            self.tableWidget.setItem(numrows[i], 0, QTableWidgetItem(str(lists[i])))
            QtCore.QTimer.singleShot(1000,self.loop.quit)
            self.loop.exec_()





        

main = MainWindow()
