from PIL import  Image
import os
import pandas as pd
import numpy as np
import colorsys

path = './dataset/clothing/'
file_number = 1006

def rgb2HsvHistogram(image):
    width, height = image.size
    hsvHistogram = [[0 for i in range(361)] for j in range(3)]
    pixel = image.load()
    for i in range(width):
        for j in range(height):
            # rgb or gray
            r, g, b = (pixel[i,j] if image.mode=='RGB' else [pixel[i,j]]*3) 
            h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
            h, s, v = int(h*360), int(s*100), int(v*255)
            hsvHistogram[0][h] += 1
            hsvHistogram[1][s] += 1
            hsvHistogram[2][v] += 1
    return hsvHistogram

os.remove("./dataset/HsvHistogram.csv") if os.path.exists("./dataset/HsvHistogram.csv") else None

with open("./dataset/HsvHistogram.csv",'a') as save:
    for i in xrange(0, file_number):
        full_name = path + 'ukbench' + '0'*(5-len(str(i))) + str(i) + '.jpg'
        file_name = 'ukbench' + '0'*(5-len(str(i))) + str(i) + '.jpg'
        print full_name
        im = Image.open(full_name)
        HsvHist = rgb2HsvHistogram(im)
        data = pd.DataFrame(HsvHist)
        data.to_csv(save, header=True,index_label=file_name)
