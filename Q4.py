
# coding: utf-8
import sift
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise

BOF_preprocess_done = False
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

# edited
def findTopTen(score_lst):
    index = [x for x in range(0, len(score_lst))]
    score_lst = zip(index, score_lst)
    list.sort(score_lst, key= lambda tup: tup[1], reverse= True)
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
    return (visual_vocabulary, codewords)

# edited
def search(target, vocabulary, codewords, swIndices): 
    target_sift  = sift.read_features_from_file(path + target.split('.')[0][-5:] + '.sift')[1]
    target_vector = turnPredictToHistgram(vocabulary.predict(target_sift), n_clusters)
    target_vector = stopwordsRemoved(target_vector, swIndices)
    score_list = calculateDistance(target_vector, codewords)
    return findTopTen(score_list)

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

"""
if not BOF_preprocess_done:
    vocabulary, codewords = BOF_preprocessing()
    BOF_preprocess_done = True
refinedCodewords, stopWordIndices = stopWords_preprocessed(5, codewords)
res = search('ukbench00000.jpg', vocabulary, refinedCodewords, stopWordIndices)
print res
"""