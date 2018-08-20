import sys
from pprint import pprint
from PyQt5 import QtWidgets, QtGui, QtCore, Qt
from PyQt5.QtWidgets import QGridLayout,QLabel, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QMainWindow, QAction, qApp, QApplication
from PyQt5.QtGui import QIcon

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

        tableWidget = QTableWidget(self)
        tableWidget.setColumnCount(6)
        tableWidget.setRowCount(1)
        tableWidget.setHorizontalHeaderLabels(["No","Time","Source","Destination","Protocol","Info"])
 
        # Fill the first line
        tableWidget.setItem(0, 0, QTableWidgetItem("Text in column 1"))
        tableWidget.setItem(0, 1, QTableWidgetItem("Text in column 2"))
        tableWidget.setItem(0, 2, QTableWidgetItem("Text in column 3"))
        

        #tableWidget.setGeometry(5,60,990,450)

        header = tableWidget.horizontalHeader()       
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.Stretch)
        #tableWidget.resizeColumnsToContents()
        grid_layout.addWidget(tableWidget,0,0)
        

main = MainWindow()