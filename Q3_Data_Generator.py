#!/usr/bin/env python
#-*- coding: utf-8 -*-

from PIL import ImageTk, Image
import os
import pandas
import sift
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise

path = './dataset/sift/'
n_clusters = 50
file_number = 1005

os.remove("./dataset/Q3.csv") if os.path.exists("./dataset/Q3.csv") else None

sift_bag  = sift.read_features_from_file('./dataset/sift/00000.sift')[1]
for i in xrange(1, file_number+1):
    file_name = path + '0'*(5-len(str(i))) + str(i) + '.sift'
    sift_bag = np.append(sift_bag, sift.read_features_from_file(file_name)[1], axis=0)
visual_vocabulary = KMeans(n_clusters=n_clusters, random_state=0).fit(sift_bag)

    #codewords = list()
with open("./dataset/Q3.csv",'a') as save:
    for i in xrange(0, file_number+1):
        count = [0 for j in xrange(n_clusters)]
        file_name = path + '0'*(5-len(str(i))) + str(i) + '.sift'
        vocList = visual_vocabulary.predict(sift.read_features_from_file(file_name)[1])
        #codewords.append(visual_vocabulary.predict(sift.read_features_from_file(file_name)[1]))
        for j in vocList:
            count[j] += 1
        data = pandas.DataFrame(count)
        data.to_csv(save,header=True,index_label = file_name[-10:])

#for i in xrange(len(codewords)):
#        codewords[i] = turnPredictToHistgram(codewords[i], n_clusters)

