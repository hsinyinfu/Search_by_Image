
# coding: utf-8
import sift
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise

BOF_preprocessing_done = False
path = './dataset/sift/'
n_clusters = 50
file_number = 1005

def zero_list_maker(n):
    zeroList = [0]*n
    return zeroList

def accumulate(lst, n_clusters):
    result = zero_list_maker(n_clusters)
    for i in xrange(len(lst)):
        result[lst[i]] = result[lst[i]]+1
    return result

def turnPredictToHistgram(predict, n_clusters):
    predict = accumulate(predict, n_clusters)
    return predict

def findTopTen(score_lst):
    index = [x for x in range(0, len(score_lst))]
    score_lst = zip(index, score_lst)
    list.sort(score_lst, key= lambda tup: tup[1], reverse= True)
    result = score_lst[:10]
    return [[indexToJPGName(index), score] for (index, score) in score_lst[:10]]

def indexToJPGName(index):
    return 'ukbench' + '0'*(5-len(str(index))) + str(index) + '.jpg'

def calculateDistance(target, codewords): # both target and codewords are list
    codewords.insert(0, target)
    return pairwise.cosine_similarity(np.array(codewords))[0][1:]

def BOF_preprocessing():
    sift_bag  = sift.read_features_from_file('./dataset/sift/00000.sift')[1]
    for i in xrange(1, file_number+1):
        file_name = path + '0'*(5-len(str(i))) + str(i) + '.sift'
        sift_bag = np.append(sift_bag, sift.read_features_from_file(file_name)[1], axis=0)
    visual_vocabulary = KMeans(n_clusters=n_clusters, random_state=0).fit(sift_bag)
    codewords = list()
    for i in xrange(0, file_number+1):
        file_name = path + '0'*(5-len(str(i))) + str(i) + '.sift'
        codewords.append(visual_vocabulary.predict(sift.read_features_from_file(file_name)[1]))
    for i in xrange(len(codewords)):
        codewords[i] = turnPredictToHistgram(codewords[i], n_clusters)
    print 'this'
    print len(codewords)
    print len(codewords[0])
    return (visual_vocabulary, codewords)

def search(target, vocabulary, codewords): #
    target_sift  = sift.read_features_from_file(path + target.split('.')[0][-5:] + '.sift')[1]
    target_vector = turnPredictToHistgram(vocabulary.predict(target_sift), n_clusters)
    score_list = calculateDistance(target_vector, codewords)
    return findTopTen(score_list)

