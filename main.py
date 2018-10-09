
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 26 21:05:17 2018

@author: jkevangelio
"""


import sys
from pprint import pprint
from PyQt5 import *

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import threading
from scapy.all import *
from scapy.all import DNS
from scapy.all import IP
from scapy.all import sniff
from datetime import datetime



class WorkerSignals(QObject):
    sig1=pyqtSignal(str,str,str,str,str)


class QThread1(QRunnable):
    
    def __init__(self,parent=None):
        super(QThread1,self).__init__()
        
        self.signals = WorkerSignals()
       
    def querysniff(self,pkt):
        
        if IP in pkt:
            ip_src = pkt[IP].src   #get the ip source address from the packets
            ip_dst = pkt[IP].dst   #get the ip destination address from the packets
            ip_proto=pkt[IP].proto #get the protocol in bytes
            time = datetime.now()
            hour = time.strftime("%H")
            minute = time.strftime("%M")
            sec = time.strftime("%S")
            rtime = (hour + ":" + minute + ":" + sec)
            
            if pkt.haslayer(DNS) and pkt.getlayer(DNS).qr == 0:
                
                if str(ip_proto)=="17":
                    ip_proto="UDP"      
                    return self.signals.sig1.emit(str(rtime),str(ip_src),str(ip_dst),str(ip_proto),str(pkt.getlayer(DNS).qd.qname))
                elif str(ip_proto)=="6":
                    ip_proto="TCP"
                    return self.signals.sig1.emit(str(rtime),str(ip_src),str(ip_dst),str(ip_proto),str(pkt.getlayer(DNS).qd.qname))
                elif str(ip_proto)=="1":
                    ip_proto="ICMP"
                    return self.signals.sig1.emit(str(rtime),str(ip_src),str(ip_dst),str(ip_proto),str(pkt.getlayer(DNS).qd.qname))
            
            elif pkt.haslayer(IP):
                pckt_ttl=pkt[IP].ttl
                if str(ip_proto)=="1":
                    ip_proto="ICMP"
                    return self.signals.sig1.emit(str(rtime),str(ip_src),str(ip_dst),str(ip_proto), "Time to Live:"+str(pckt_ttl))
                elif str(ip_proto)=="6":
                    ip_proto="TCP"
                    return self.signals.sig1.emit(str(rtime),str(ip_src),str(ip_dst),str(ip_proto), "Time to Live:"+str(pckt_ttl))
                elif str(ip_proto)=="17":
                    ip_proto="UDP"
                    return self.signals.sig1.emit(str(rtime),str(ip_src),str(ip_dst),str(ip_proto), "Time to Live:"+str(pckt_ttl))
                    
            
            
    def stop_sniffing(self,x):
        global switch
        return switch
            
    def sniffing(self):
        
        if radio.isChecked():
            button="enp0s3"
        elif radio2.isChecked():
            button="enp0s8"
            
        print("Thread Start")
        
        sniff(iface = button, stop_filter=self.stop_sniffing, prn = self.querysniff, store = 0)
        
        print("\n[*] Shutting Down...")      
    
    
    @pyqtSlot()
    def run(self):
        
        global switch
        self.thread = threading.Thread(target=self.sniffing)
        if (self.thread is None) or (not self.thread.is_alive()):
            switch = False
            self.thread.start()
        else:
            print("already running!")
        


class MainWindow(QMainWindow):
    
    TIME,SOURCE,DEST,PRO,DNS = range(5)
    
    def __init__(self):
        self.app = QApplication(sys.argv)
        super().__init__()

        self.initWindow()
        
    def initWindow(self):
        self.setWindowTitle("WhiteShark")
        self.statusBar().showMessage("This is a status bar")
        self.setGeometry(200,100,1000,500 )
        
        self.pool=QThreadPool()
        
        self.toolbar = self.addToolBar("Save")

        self.capture_action = QAction(QIcon("images/capture.png"), "&Capture", self)
        self.capture_action.setShortcut("Ctrl+C")
        self.capture_action.setStatusTip("Capture")
        self.capture_action.triggered.connect(self.on_but1)

        self.stop_action = QAction(QIcon("images/stop.png"), "&Stop", self)
        self.stop_action.setShortcut("Ctrl+S")
        self.stop_action.setStatusTip("Stop")
        self.stop_action.triggered.connect(self.on_but2)

        self.exit_action = QAction(QIcon("images/exit.png"), "&Exit", self)
        self.exit_action.setShortcut("Ctrl+q")
        self.exit_action.setStatusTip("Exit program")
        self.exit_action.triggered.connect(qApp.quit)
        
        self.checkip = QLineEdit(self)
        self.checkip.setPlaceholderText("Enter IP address to check")

        self.checkbut =  QPushButton('Check',self)
        self.checkbut.clicked.connect(self.showpop)
        
        
        global radio 
        radio= QRadioButton("enp0s3")
        radio.setChecked(True)
        radio.toggled.connect(lambda:self.btnstate(radio))
        
        
        global radio2
        radio2= QRadioButton("enp0s8")
        radio2.toggled.connect(lambda:self.btnstate(radio2))
        

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(self.capture_action)
        fileMenu.addAction(self.stop_action)
        fileMenu.addAction(self.exit_action)
        


        self.toolbar.addAction(self.capture_action)
        self.toolbar.addAction(self.stop_action)
        self.toolbar.addAction(self.exit_action)
        
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        grid_layout = QGridLayout(self)
        central_widget.setLayout(grid_layout)

        self.dataView = QTreeView()
        self.dataView.setRootIsDecorated(False)
        self.dataView.setAlternatingRowColors(True)
        self.model = self.createModel(self)
        self.dataView.setModel(self.model)
        
        
        grid_layout.addWidget(self.checkip,0,0,1,3)
        grid_layout.addWidget(self.checkbut,0,3,1,1)
        grid_layout.addWidget(radio,0,4,1,2)
        grid_layout.addWidget(radio2,0,6,1,3)
        grid_layout.addWidget(self.dataView,1,0,5,14)
        
        self.show()
        sys.exit(self.app.exec_())
        
        
        
    def btnstate(self,b):
        
        if b.text()=="enp0s3":
            if b.isChecked()==True:
                button="enp0s3"
                print(button)
        elif b.text()=="enp0s8":
            if b.isChecked()==True:
                button="enp0s8"
                print(button)
        else:
            button = "enp0s3"
            
                
    def createModel(self,parent):
        
        model = QStandardItemModel(0,5, parent)
        model.setHeaderData(self.TIME, Qt.Horizontal,"Time")
        model.setHeaderData(self.SOURCE, Qt.Horizontal, "Source")
        model.setHeaderData(self.DEST, Qt.Horizontal, "Destination")
        model.setHeaderData(self.PRO, Qt.Horizontal,"Protocol")
        model.setHeaderData(self.DNS, Qt.Horizontal,"Information")
        
        return model
    
    def addcontent(self,model,time,source,dest,proto,dns):
        
        model.insertRow(0)
        model.setData(model.index(0,self.TIME),time)
        model.setData(model.index(0,self.SOURCE),source)
        model.setData(model.index(0,self.DEST),dest)
        model.setData(model.index(0,self.PRO),proto)
        model.setData(model.index(0,self.DNS),dns)
    
    def on_info(self,timee,source,dest,proto,dns):
        self.addcontent(self.model,timee,source,dest,proto,dns)
        
    def on_but1(self):
        self.thread = QThread1()
        self.pool.start(self.thread)
        self.thread.signals.sig1.connect(self.on_info)
        self.capture_action.setEnabled(False)
        
    def on_but2(self):
        
        global switch
        print("stopping")
        switch = True
        self.capture_action.setEnabled(True)
        
    def showpop(self):
        name = self.checkip.text()
        conf.verb = 0
        result=""
        packet = IP(dst = name, ttl=20)/ICMP()
        reply = sr1(packet, timeout = 2)
        if not (reply is None):
            result=str(reply.src+" is online")
        else:
            result=str(str(name)+" is offline")
        self.exPop = popup(result)
        
        self.exPop.show()
        
        
class popup(QWidget):
    def __init__(self,name):
        super().__init__()
        self.name=name
        self.initUI()
        self.setGeometry(200,100,500,250)
    def initUI(self):
        lblName=QLabel(self.name,self)



main = MainWindow()
