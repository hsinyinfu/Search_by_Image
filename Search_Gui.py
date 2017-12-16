#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from pylab import *

import pickle

from Tkinter import *
from PIL import ImageTk, Image
import tkMessageBox
import tkFileDialog 
from ttk import Frame, Button, Label, Style

from random import randint
from PIL import Image

class Example(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent
        
        self.initUI()
    
        
    def initUI(self):
      
        self.parent.title("HW3") 

        self.pack(fill=BOTH, expand=1)

        Button(self, text = "Select File", command = openFile).grid(row=0, column=0, pady=5)
        self.fileName = StringVar()
        Label(self, textvariable=self.fileName).grid(row=0, column=1, columnspan=2, pady=5, sticky=W)

        Label(self, text = "Select Mode: ").grid(row=1, column=0, pady=5)
        mode = StringVar(self)
        mode.set("Q1-ColorHistogram")
        om = OptionMenu(self, mode, "Q1-ColorHistogram", "Q2-ColorLayout", "Q3-SIFT Visual Words", "Q4-Visual Words using stop words")
        om.grid(row=1, column=1, pady=5, sticky=W)

        Button(self, text = "SEARCH", command = lambda: startSearching(self.fileName.get(),mode.get())).grid(row=3, column=0, pady=5)

        self.images = []
        for i in range(10):
            self.images.append(Label(self))
            self.images[i].grid(row=i/5+4, column=i%5, pady=50)


 
def openFile ():
    fileName = tkFileDialog.askopenfilename(initialdir = "./dataset")
    app.fileName.set(fileName)

def startSearching (fileName, mode):
    print "Your Code Here."


if __name__ == '__main__':
    root = Tk()
    size = 220, 220

    app = Example(root)
    root.geometry("1024x720")
    root.mainloop()

  