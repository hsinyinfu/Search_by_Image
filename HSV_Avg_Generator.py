from PIL import  Image
import os
import pandas as pd
import numpy as np
import colorsys

path = './dataset/clothing/'
file_number = 1006

def rgb2HsvAvg(image):
    avg = [0, 0, 0]
    width, height = image.size
    pixel = image.load()
    for i in range(width):
        for j in range(height):
            # rgb or gray
            r, g, b = (pixel[i,j] if image.mode=='RGB' else [pixel[i,j]]*3) 
            h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
            h, s, v = int(h*360), int(s*100), int(v*255)
            avg[0] += h
            avg[1] += s
            avg[2] += v
    pixelNum = width * height
    for i in range(len(avg)):
        avg[i] /= pixelNum
    return avg

os.remove("./dataset/HsvAvg.csv") if os.path.exists("./dataset/HsvAvg.csv") else None

with open("./dataset/HsvAvg.csv",'a') as save:
    for i in xrange(0, file_number):
        full_name = path + 'ukbench' + '0'*(5-len(str(i))) + str(i) + '.jpg'
        file_name = 'ukbench' + '0'*(5-len(str(i))) + str(i) + '.jpg'
        print full_name
        im = Image.open(full_name)
        imAvg = rgb2HsvAvg(im)
        data = pd.DataFrame(imAvg)
        data.to_csv(save, header=True,index_label=file_name)
