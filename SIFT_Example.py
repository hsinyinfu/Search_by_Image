#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image
from numpy import array
import sift
from pylab import *


imname = 'Penguins.jpg'

im1 = array(Image.open(imname).convert('L'))

sift.process_image(imname,'Penguins.sift')

l1,d1 = sift.read_features_from_file('Penguins.sift')
figure()
gray()
sift.plot_features(im1,l1,circle=True)
show()

