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
#imname = 'Penguins.jpg'
imname =  'ukbench00000.jpg'
for imname in dataset:
    #print(imname)
#im1 = array(Image.open(path+imname).convert('L'))
    sift.process_image(path+imname,outPath + imname[7:-4] + '.sift')

#l1,d1 = sift.read_features_from_file(outPath+imname[7:-4] + '.sift')
#figure()
#gray()
#sift.plot_features(im1,l1,circle=True)
#show()

