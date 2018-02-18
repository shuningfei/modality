#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import pickle
from europarl import *
from util import *

if __name__ == '__main__':
	
	europarlFiles = ['../EPOS/en-de.pos-pts.txt','../EPOS/DE_intersect00.txt', '../EPOS/DE_intersect01.txt']

	scheint = ["scheinen","scheine","scheinst","scheint","schien","schienst","schienen","schient","scheinest","scheinet","scheinend","geschienen"]
	bestimmt = ["bestimmt"]
	vielleicht = ["vielleicht"]
	moeglicherweise = ["möglicherweise"]
	wohl = ["wohl"]
	womoeglich = ["womöglich"]
	eventuell = ["eventuell"]
	wahrscheinlich = ["wahrscheinlich","unwahrscheinlich"]
	sicher = ["sicher"]
	vermutlich = ["vermutlich"]
	sicherlich = ["sicherlich"]

	erlauben = ["erlaube", "erlaubst", "erlaubt", "erlauben", "erlaubte", "erlaubtest", "erlaubten", "erlaubtet"]
	gestatten = ["gestatte", "gestattest", "gestattet", "gestatten", "gestattete", "gestattetest", "gestatteten", "gestattetet", "gestattend"]
	brauchen = ["brauche", "brauchst", "braucht", "brauchen", "brauchte", "brauchtest", "brauchten", "brauchtet", "gebraucht", "brauchest", "brauchet", "brauch", "brauchend"]
	bedarf = ["bedarf", "bedarfst", "bedürfen", "bedürft", "bedürfe", "bedürfest", "bedürfet", "bedurft", "bedurfte", "bedurftest", "bedurften", "bedurftet", "bedürfte", "bedürftest", "bedürften", "bedürftet", "bedurft"]
	unbedingt = ["unbedingt"]
	erforderlich = ["erforderlich", "erfordere", "erforderst", "erfordert", "erfordern", "erforderte", "erfordertest", "erforderten", "erfordertet", "erfordere", "erforderest", "erforderet", "erfordernd"]
	benoetigen = ["benötige", "benötigst", "benötigt", "benötigen", "benötigest", "benötiget", "benötig", "benötigte", "benötigtest", "benötigten", "benötigtet", "benötigend"]
	besser = ["besser"]
	lieber = ["lieber"]
	hoffentlich = ["hoffentlich"]

	schaffen = ["geschafft", "geschaffen", "schaffe", "schaffst", "schafft", "schaffen", "schuf", "schufst", "schufen", "schüfe", "schüfest", "schüfen", "schüfet", "schaffend"]
	gelingen = ["gelinge", "gelingst", "gelingt", "gelingen", "gelang", "gelangst", "gelangen", "gelangt", "gelungen", "gelingest", "gelinget", "gelänge", "gelängest", "gelängen", "gelänget", "geling", "gelingend"]
	bar = ["erkennbar","machbar","vergleichbares","vorstellbar","realisierbar","erneuerbarer","vermeidbar","vermeidbare"]

	seedsGe=[scheint,bestimmt,vielleicht,moeglicherweise,wohl,womoeglich,eventuell,wahrscheinlich,sicher,vermutlich,sicherlich,erlauben,gestatten,brauchen,bedarf,unbedingt,erforderlich,benoetigen,besser,lieber,hoffentlich,schaffen,gelingen,bar]
	seedsGeFull = []

	for sg in seedsGe:
		sgFull = []
		for s in sg:
			sgFull.append(s)
			sgFull.append(s[0].upper()+s[1:len(s)])

		seedsGeFull.append(sgFull)

	print seedsGeFull


	countResAll=[]
	for sg in seedsGeFull:
		countRes={}
		countResAll.append(countRes)
	
	for europarlFile in europarlFiles:
		#spoSet = set([])
		f = open(europarlFile)
		lines = f.readlines()				
		
		for line in lines:
			spo = SentencePair(line)
			#print spo

			#spoSet.add(spo)		
		
		#for spo in spoSet:	
			typeInfo = spo.translationType('geToEn')
			sourceLanguage = typeInfo[0]
			sourceAlign = typeInfo[1]
			targetLanguage = typeInfo[2]
			targetAlign = typeInfo[3]
			
			for i in range(len(seedsGeFull)):
				countResAll[i] = spo.getTranslationStatistic(seedsGeFull[i],countResAll[i],sourceLanguage,sourceAlign,targetLanguage,targetAlign)

	#output = open('countList.pkl', 'wb')
	#pickle.dump(countResAll, output)

	"""
	for pair in zip(countResAll,seedsGeFull):
		countResList = sorted(pair[0].iteritems(), key=lambda d:d[1], reverse = True)
		writeStatisticResult("trainStat/"+str(pair[1][0])+".txt", countResList)
	"""