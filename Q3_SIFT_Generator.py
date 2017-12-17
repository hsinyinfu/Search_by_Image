#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from PIL import Image
from numpy import array
import sift
from pylab import *


path = "./dataset/clothing/"
path,dirs,dataset = os.walk(path).next()
outPath = "./dataset/sift/"
for imname in dataset:
    outName = outPath + imname[7:-4] + '.sift'
    sift.process_image(path + imname, outName)

    edge = 150
    peak = 3
    while(os.path.getsize(outName) <=  500):
        parameter = "--edge-thresh "+str(edge)+" --peak-thresh "+str(peak)
        sift.process_image(path + imname, outName, parameter)

