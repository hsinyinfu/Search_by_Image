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
import Q3

global imgs
global thumb

BOF_preprocess_done = False

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
        
        self.fileName = StringVar(value = "./dataset/clothing/ukbench00000.jpg")
        albl = Label(self, textvariable = self.fileName)
        albl.grid(row=0, column=2, columnspan=3, pady=5, sticky=W)

        self.thumb = Label(self)
        self.thumb.grid(row=0, column=1, pady=5, sticky=W)
        image = Image.open(self.fileName.get())
        image = ImageTk.PhotoImage(image.resize((image.size[0]/2, image.size[1]/2),Image.ANTIALIAS))
        self.thumb.configure(image = image)
        self.thumb.image = image
        
        
        # Mode
#        clbl = Label(self, text = "-- Select Mode --")
#        clbl.grid(row=2, column=0, pady=5)
        mode = StringVar(self)
        mode.set('-- Select Mode --')
        menu = OptionMenu(self, mode, 'Q1-Color_Histogram', 'Q2-Color_Layout',
                          'Q3-SIFT_Visual_Words', 'Q4-Visual_Words_Using_Stop_Words')
        menu.grid(row=1, column=0, pady=5, sticky=W)
        
        # Start Searching
        dbtn = Button(self, text = "START SEARCHING", command = lambda: startSearching(mode.get(),self.fileName.get()))
        dbtn.grid(row=1, column=1, pady=5, sticky=W)

        # Return Ranking List
        self.imgs = []
        for i in xrange(10):
            self.imgs.append(Label(self))
            self.imgs[i].grid(row = i / 5 + 4, column = i % 5 , padx=10, pady=20)

def openFile():
    fileName = tkFileDialog.askopenfilename(initialdir = "./dataset/clothing/")
    app.fileName.set(fileName)
    image = Image.open(app.fileName.get())
    image = ImageTk.PhotoImage(image.resize((image.size[0]/2, image.size[1]/2),Image.ANTIALIAS))
    app.thumb.configure(image = image)
    app.thumb.image = image

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

def Q2_CountDistance(query, base, weight):
    #Eular Distance
    dis  = 0
    for i in xrange(1,len(query)):
        dis += weight[i-1] / 10 * pow(float(query[i]) - float(base[i]),2)
    return sqrt(dis)

def maxInList(list):
    max = [0,0.0] #[index,value]
    for l in list:
        if l[1] > max[1]:
            max = [list.index(l),l[1]]
    return max[0]

def startSearching(mode,fileName):
    #path = "./dataset/clothing/"
    #query = Image.open(path + fileName)
    #print fileName[:-16]
    query = Image.open(fileName)
    path,dirs,dataset = os.walk(fileName[:-16]).next()
    fileName = fileName[-16:]
    #print fileName
    res = []
    if mode[1] == "-":
        return -1
    elif mode[1] == "1":      #Q1-Color_Histogram
        
        res = [["",1.0] for i in xrange(10)] #[fileName,distance]
        for imgName in dataset:
            img = Image.open(path+'/'+imgName)
            distance = Q1_CountDistance(query,img)
            #print distance
            index = maxInList(res)
            if distance < res[index][1]:
                res[index] = [imgName,distance]
        res = sorted(res,key = lambda x: x[1])

    elif mode[1] == "2":    #Q2-Color_Layout

        res = [["",float("inf")] for i in xrange(10)] #[fileName,distance]
        qIndex = int(fileName[7:-4]) * 4 #Query index
        with open('./dataset/Q2.csv', 'rb') as csvfile:
            Q2Reader = csv.reader(csvfile)
            data = [row for row in Q2Reader]
            for row in xrange(0,len(data),4):
                distance = 0
                for i in xrange(0,4):
                    distance += Q2_CountDistance(data[qIndex+i], data[row+i], [j for j in xrange(len(data[0])-1,0,-1)])
                index = maxInList(res)
                #print res[index][1]
                if distance < res[index][1]:
                    res[index] = [data[row][0],distance]
        res = sorted(res,key = lambda x: x[1])

    elif mode[1] == "3":    #Q3-SIFT_Visual_Words
        global BOF_preprocess_done
        if not BOF_preprocess_done:
            vocabulary, codewords = Q3.BOF_preprocessing()
            BOF_preprocess_done = True
        #print codewords[0]
        res = Q3.search(fileName, vocabulary, codewords)
        #print res


    elif mode[1] == "4":    #Q4-Visual_Words_Using_Stop_Words
        print "4"

    print "### Query: " + fileName + " / " + mode
    print res

    for i in xrange(10):
        imgName = path + res[i][0]
#        image = ImageTk.PhotoImage(Image.open(imgName))
        image = Image.open(imgName)
        image = ImageTk.PhotoImage(image.resize((int(image.size[0]*0.85), int(image.size[1]*0.85)),Image.ANTIALIAS))
        app.imgs[i].configure(image = image)
        app.imgs[i].image = image

if __name__ == '__main__':
    root = Tk()
    size = 540, 720

    app = Example(root)
    root.geometry("1920x1080")
    root.mainloop()

  
