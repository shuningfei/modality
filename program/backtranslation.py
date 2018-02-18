#!/usr/bin/python
# -*- coding: utf-8 -*-

import pickle
from probability import seedsGeFull

countDictList_file = open("countList.pkl","rb")

countDictList = pickle.load(countDictList_file)


#print len(countDictList)
#print countDictList



# calculate total count of all paraphrases.
def getParaphraseTotalCount(countDictList):

  #print countDictList

  #print len(countDictList)

  count_back = {}

  for ele in countDictList:
    for para in ele.keys():
      if not count_back.has_key(para):
        count_back[para] = ele[para]
      else:
        count_back[para] += ele[para]
      
  count_back_sorted = sorted(count_back.iteritems(), key=lambda d:d[1], reverse = True)

  #print count_back_sorted
  return count_back_sorted

# calculate
def getBackProb(countDictList):
  probAll = []
  count_back_sorted = getParaphraseTotalCount(countDictList)
  for seed in countDictList:
    probList = []
    for ele in count_back_sorted:
      para = ele[0]
      for paraInBigList in seed.keys():
        if para == paraInBigList:
          count = seed[para]
          prob = seed[para]/float(ele[1])
          probList.append((para,prob,count))
    probListSorted = sorted(probList, key=lambda d:d[1], reverse = True)

    #print probListSorted
    probAll.append(probListSorted)
  #print len(probAll)
  return probAll

def writeBackProb(countDictList):
  probAll = getBackProb(countDictList)
  for pair in zip(seedsGeFull,probAll):
    fw = open('backtrans2/'+pair[0][0]+".txt",'w')
    for p in pair[1]:
      if p[2] >10:
        fw.write(p[0]+"\t"+str(p[1])+"\t"+str(p[2])+"\n")
	
def cateStat(probCate):
  
  count_cate = {}
  
  for seeds in probCate:
    
    for paragroup in seeds:
      
      if not count_cate.has_key(paragroup[0]):
        count_cate[paragroup[0]] = paragroup[2]
      else:
        count_cate[paragroup[0]] += paragroup[2]
  
  return count_cate

def cateProb(count_back_sorted,count_cate):
  
  probList = []
  for ele in count_back_sorted:
    para = ele[0]
    for paraInCount in count_cate.keys():
      if paraInCount == para:
        count = count_cate[para]
        prob = count/float(ele[1])
        probList.append((para,prob,count))

  probListSorted = sorted(probList, key=lambda d:d[1], reverse = True)
  return probListSorted

def writeProbCate(cateFlag,count_back_sorted,count_cate):
  
  fw = open('backTransCate/'+cateFlag+'.txt','w')
  
  probListSorted = cateProb(count_back_sorted,count_cate)
  
  for p in probListSorted:
      if p[2] >10:
        fw.write(p[0]+"\t"+str(p[1])+"\t"+str(p[2])+"\n")

  
def getBackProbCate(countDictList):
  
  # 0-10: ep
  # 11-20: de
  # 21-23: dy
  
  # print len(probAll[:11])
  # print len(probAll[11:21])
  # print len(probAll[21:])
  
  probAll = getBackProb(countDictList)
  
  probEp = probAll[:11]
  probDe = probAll[11:21]
  probDy = probAll[21:]
  
  count_cate_ep = cateStat(probEp)
  count_cate_de = cateStat(probDe)
  count_cate_dy = cateStat(probDy)
  
  count_back_sorted = getParaphraseTotalCount(countDictList)
  
  writeProbCate('ep',count_back_sorted,count_cate_ep)
  writeProbCate('de',count_back_sorted,count_cate_de)
  writeProbCate('dy',count_back_sorted,count_cate_dy)
  

  
  #print ep
 
  """
  for seeds in ep:
    
    for paragroup in seeds:
      
      if not count_cate_ep.has_key(paragroup[0]):
	count_cate_ep[paragroup[0]] = paragroup[2]
      else:
	count_cate_ep[paragroup[0]] += paragroup[2]
   """
  
  
  #print count_cate_ep
  
  

"""
def getBackProb(countDictList):
  count_back_sorted = getParaphraseTotalCount(countDictList)
  for pair in zip(seedsGeFull,countDictList):
    fw = open('backtrans/'+pair[0][0]+".txt",'w')
    probList = []
    for ele in count_back_sorted:
      para = ele[0]
      for paraInBigList in pair[1].keys():
	if para == paraInBigList:
	  count = pair[1][para]
	  prob = pair[1][para]/float(ele[1])
	  probList.append((para,prob,count))
    probListSorted = sorted(probList, key=lambda d:d[1], reverse = True)   
    for p in probListSorted:
      if p[2] >10:
	fw.write(p[0]+"\t"+str(p[1])+"\t"+str(p[2])+"\n")
"""
#def getBackProbCate(countDictList):
  

#if __name__ == '__main__':
  #getBackProbCate(countDictList)

  #getParaphraseTotalCount(countDictList)

  #getBackProbCate(countDictList)
    


  