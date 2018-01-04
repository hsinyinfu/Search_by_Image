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

global imgs
global thumb


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
    dis = 0
    for i in xrange(1,len(query)):
        dis += weight[i-1] / 10 * pow(float(query[i]) - float(base[i]),2)
    return sqrt(dis)

def Q3Q4_CountDistance(target, codewords): # both target and codewords are list
    from sklearn.metrics import pairwise
    import numpy as np
    
    codewords.insert(0, target)
    scoreList = pairwise.cosine_similarity(np.array(codewords))[0][1:]
    return scoreList

def findStopWords(stopWordNum, codewordsHist):
    sumHistogram = np.zeros(len(codewordsHist[0])).astype('int')
    for i in codewordsHist:
        sumHistogram = sumHistogram + np.array(i).astype('int')
    index = [x for x in range(0, len(sumHistogram))]
    freq_lst = zip(index, sumHistogram)
    list.sort(freq_lst, key= lambda tup: tup[1], reverse= True)
    return [x[0] for x in freq_lst[:stopWordNum]]

def stopwordsRemoved(lst, swIndices):
    descending = sorted(swIndices, reverse=True)
    refinedLst = list()
    for index in descending:
        refinedLst = lst[:index] + lst[index+1:]
        lst = refinedLst
    return refinedLst

def stopWords_preprocessed(stopWordNum, codewords):
    stopWordIndices = findStopWords(5, codewords)
    refinedCodewords = list()
    for i in xrange(len(codewords)):
        refinedCodewords.append(stopwordsRemoved(codewords[i], stopWordIndices))
    return (refinedCodewords, stopWordIndices)

def maxInList(list):
    max = [0,0.0] #[index,value]
    for l in list:
        if l[1] > max[1]:
            max = [list.index(l),l[1]]
    return max[0]

def minInList(list):
    min = [0,float("inf")] #[index,value]
    for l in list:
        if l[1] < min[1]:
            min = [list.index(l),l[1]]
    return min[0]

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
        
        res = [["",float("inf")] for i in xrange(10)] #[fileName,distance]
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
        res = []
        n_clusters = 50
        with open('./dataset/Q3.csv', 'rb') as voc:
            vocReader = csv.reader(voc)
            qIndex = int(fileName[7:-4]) * (n_clusters+1)
            data = [row for row in vocReader]
            base = []

            for row in xrange(0,len(data),n_clusters+1):
                b = [0 for i in xrange(n_clusters)]
                for i in xrange(n_clusters):
                    b[i] = int(data[row+i+1][1])
                base.append(b)
            
            query = []
            for i in xrange(qIndex+1,qIndex+1+n_clusters):
                query.append(int(data[i][1]))
    
        scoreList = Q3Q4_CountDistance(query, base)
        for x in xrange(0, len(scoreList)):
            res.append(['ukbench'+data[x*(n_clusters+1)][0][:-4]+'jpg',scoreList[x]])
        res = sorted(res,key = lambda x: x[1],reverse=True)[:10]

    elif mode[1] == "4":    #Q4-Visual_Words_Using_Stop_Words
        res = []
        n_clusters = 50
        with open('./dataset/Q3.csv', 'rb') as voc:
            vocReader = csv.reader(voc)
            qIndex = int(fileName[7:-4]) * (n_clusters+1)
            data = [row for row in vocReader]
            base = []
            
            for row in xrange(0,len(data),n_clusters+1):
                b = [0 for i in xrange(n_clusters)]
                for i in xrange(n_clusters):
                    b[i] = int(data[row+i+1][1])
                base.append(b)
            refineBase, stopWordIndices = stopWords_preprocessed(5, base)

            query = []
            for i in xrange(qIndex+1,qIndex+1+n_clusters):
                query.append(int(data[i][1]))
            
            newQuery = stopwordsRemoved(query,stopWordIndices)

        scoreList = Q3Q4_CountDistance(newQuery, refineBase)
        for x in xrange(0, len(scoreList)):
            res.append(['ukbench'+data[x*(n_clusters+1)][0][:-4]+'jpg',scoreList[x]])
        res = sorted(res,key = lambda x: x[1],reverse=True)[:10]


    print "#  Query: " + fileName + " / " + mode
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

  
