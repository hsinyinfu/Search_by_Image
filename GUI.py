#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sys import platform as sys_pf
if sys_pf == 'darwin':
    import matplotlib
    matplotlib.use("TkAgg")

import os
from pylab import *

import pickle

from Tkinter import *
from PIL import ImageTk,Image
import tkMessageBox
import tkFileDialog
from ttk import Frame, Button, Label, Style

from random import randint

from scipy.fftpack import dct
import csv
import pandas


class Example(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()
    
    def initUI(self):
        
        self.parent.title("HW3")
        self.pack(fill=BOTH, expand=1)
        
        # File
        abtn = Button(self, text = "-- Select File --", command = openFile)
        abtn.grid(row=0, column=0, pady=5)
        
        self.fileName = StringVar(value = "ukbench00000.jpg")
        bbtn = Label(self, textvariable = self.fileName)
        #bbtn.grid(row=0, column=1, columnspan=2, pady=5, sticky=W)
        bbtn.grid(row=0, column=1, pady=5, sticky=W)
        
        # Mode
        cbtn = Label(self, text = "-- Select Mode --")
        cbtn.grid(row=1, column=0, pady=5)
        mode = StringVar(self)
        mode.set('Q1-Color_Histogram')
        menu = OptionMenu(self, mode, 'Q1-Color_Histogram', 'Q2-Color_Layout',
                          'Q3-SIFT_Visual_Words', 'Q4-Visual_Words_Using_Stop_Words')
        menu.grid(row=1, column=1, pady=5, sticky=W)
        
        # Start Searching
        dbtn = Button(self, text = "START SEARCHING", command = lambda: startSearching(mode.get(),self.fileName.get()))
        dbtn.grid(row=1, column=2, pady=5)

        # Return Ranking List
#        self.imgs = []
#        for i in xrange(10):
#            self.imgs.append(Label(self))
#            self.imgs[i].grid(row = i / 5,column = i % 5 , pady=60)



    def onSelect(self, val):
      
        sender = val.widget
        idx = sender.curselection()
        value = sender.get(idx)   

        self.var.set(value)
 
def openFile():
    fileName = tkFileDialog.askopenfilename(initialdir = "./dataset/clothing/")
    app.fileName.set(fileName)

def min(a,b):
    return a if a<b else b

def Q1_CountDistance(query, base):
    minTotal = 0
    qTotal = 0
    bTotal = 0
    queryColor = query.histogram()
    baseColor = base.histogram()
    for i in xrange(0,len(baseColor)):
        q = queryColor[i]
        b = baseColor[i]
        minTotal += min(q,b)
        qTotal += q
        bTotal += b
    return 1 - float(minTotal / float(min(qTotal,bTotal)))

def maxInList(list):
    max = [0,0.0] #[index,value]
    for l in list:
        if l[1] > max[1]:
            max = [list.index(l),l[1]]
    return max[0]



def startSearching(mode,fileName):
    path = "./dataset/clothing/"
    query = Image.open(path + fileName)
    path,dirs,dataset = os.walk(path).next()
    
    if mode[1] == "1":      #Q1-Color_Histogram
        
        res = [["",1.0] for i in xrange(10)]
        for imgName in dataset:
            img = Image.open(path+'/'+imgName)
            distance = Q1_CountDistance(query,img)
            #print distance
            index = maxInList(res)
            if distance < res[index][1]:
                res[index] = [imgName,distance]
        res = sorted(res,key = lambda x: x[1])
        print res

    elif mode[1] == "2":    #Q2-Color_Layout
        print "2"
    
    
    elif mode[1] == "3":    #Q3-SIFT_Visual_Words
        print "3"


    elif mode[1] == "4":    #Q4-Visual_Words_Using_Stop_Words
        print "4"


if __name__ == '__main__':
    root = Tk()
    size = 540, 720
#    imname = []
#    im = []
#    img = []
#
#    for i in range(10):
#        imname.append(0)
#        im.append(0)
#        img.append(0)
#
#        ### This is an example. ###
#        ### You can change your own ###
#
#        random = randint(0,103)
#
#        imname[i] = 'dataset/'  + str(random) + '.jpg'
#
#        im[i] = Image.open(imname[i])
#        im[i].thumbnail(size, Image.ANTIALIAS)
#
#        img[i] = ImageTk.PhotoImage(im[i])

    app = Example(root)
    root.geometry("1024x720")
    root.mainloop()

  
