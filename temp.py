#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 26 21:09:58 2018

@author: jkevangelio
"""

f = open("../tcpdump.txt","r")
lines = [line for line in f if line.strip()]
f.close()

#for line in range(len(lines)):
#    print(line)

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
    
print(source)
    
    
    
    


    