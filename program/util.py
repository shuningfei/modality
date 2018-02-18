#!/usr/bin/python
# -*- coding: utf-8 -*-

def sortCountList(dict):
	countListSorted = sorted(dict.iteritems(), key=lambda d:d[1], reverse = True)
	return countListSorted

def convertCountToProbabilitySorted(dict):

	countListSorted = sorted(dict.iteritems(), key=lambda d:d[1], reverse = True)
	probability = []

	total = 0
	for ele in countListSorted:
		total += int(ele[1])

	for ele in countListSorted:
		probability.append((ele[0].strip(),int(ele[1])/float(total)))

	return probability


def statistic(d,key):
	key = key.lower()
	if not d.has_key(key):
		d[key] = 0
	d[key]	 += 1
	return d

def writeContext(contextFile,contextString):
	f = open(contextFile,'w')
	f.write(contextString)
	f.close()

def makeSeedList(seedFile):
	f = open(seedFile)
	lines = f.readlines()

	epistemic = set(lines[0].strip().split(', '))
	deontic = set(lines[1].strip().split(', '))
	dynamic = set(lines[2].strip().split(', '))
	optative = set(lines[3].strip().split(', '))

	return epistemic, deontic, dynamic, optative
	
def writeStatisticResult(writeFileName, countRes):
	statisticFile = open(writeFileName,'w')
	for ele in countRes:
		statisticFile.write(ele[0]+"--"+str(ele[1])+"\n")
	statisticFile.close()
	
def writeExtrateSentence(writeFile,translationsAndMv,spo):
	i=0
	translations = translationsAndMv[0]
	if len(translations)!=0 and len(translations[0])!=0:
		for t in translations:
			writeFile.write(str(spo.id)+'\n' + translationsAndMv[1]+t+str(translationsAndMv[3])+' '+str(translationsAndMv[2]) + '\n'+" ".join(spo.wordEn) + '\n'+" ".join(spo.wordGe)+'\n'+'\n')
			i+=1
	#print i