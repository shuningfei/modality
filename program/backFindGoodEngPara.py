#!/usr/bin/python
# -*- coding: utf-8 -*-

import pickle
from europarl import *
from util import *

countDictList_file = open("countList.pkl","rb")

countDictList = pickle.load(countDictList_file)

europarlFiles = ['../EPOS/en-de.pos-pts.txt','../EPOS/DE_intersect00.txt', '../EPOS/DE_intersect01.txt']

#europarlFiles = ['../EPOS/test.txt']

def backTrains():

  for j in range(len(countDictList)):

    countResAll = []
    allPara = []
    for para in countDictList[j].keys():
      countRes = {}

      upperLower = []
      para = para.strip()
      upperLower.append(para)
      upperLower.append(para[0].upper()+para[1:len(para)])

      allPara.append(upperLower)
      countResAll.append(countRes)

    #print allPara
    #print countResAll

    for europarlFile in europarlFiles:
      f = open(europarlFile)
      lines = f.readlines()

      for line in lines:

        spo = SentencePair(line)
        typeInfo = spo.translationType('enToGe')
        sourceLanguage = typeInfo[0]
        sourceAlign = typeInfo[1]
        targetLanguage = typeInfo[2]
        targetAlign = typeInfo[3]

        for i in range(len(allPara)):
          countResAll[i] = spo.getTranslationStatistic(allPara[i],countResAll[i],sourceLanguage,sourceAlign,targetLanguage,targetAlign)

    output = open('BackLists/backTrainCountList'+str(j)+'.pkl', 'wb')

    print zip(allPara,countResAll)

    pickle.dump(countResAll,output)




"""

  for ele in countDictList:

    allPara=[]
    #countResAll=[]

    for para in ele.keys():
      #countRes={}
      #countResAll.append(countRes)
      allPara.append([para.strip()])

    allParaAll.append(allPara)

    #print len(countResAll)

  #print allParaAll

  for europarlFile in europarlFiles:
    f = open(europarlFile)
    lines = f.readlines()

    for line in lines:

      spo = SentencePair(line)
      typeInfo = spo.translationType('enToGe')
      sourceLanguage = typeInfo[0]
      sourceAlign = typeInfo[1]
      targetLanguage = typeInfo[2]
      targetAlign = typeInfo[3]

      #print sourceLanguage
      #print sourceAlign
      #print targetLanguage
      #print targetAlign

      for allPara in allParaAll:

        countResAll=[]

        for para in allPara:
          countRes={}
          countResAll.append(countRes)

        for i in range(len(allPara)):
          #print i
          countResAll[i] = spo.getTranslationStatistic(allPara[i],countResAll[i],sourceLanguage,sourceAlign,targetLanguage,targetAlign)

      countResAllAll.append(countResAll)

  output = open('backTrainBigCountList.pkl', 'wb')
  pickle.dump(countResAllAll,output)


def lookAtList():

  backTrainBigCountList_file = open("backTrainBigCountList.pkl","rb")
  backTrainBigCountList = pickle.load(backTrainBigCountList_file)

  print len(backTrainBigCountList)
"""
if __name__ == '__main__':
  backTrains()
  #lookAtList()

    


  