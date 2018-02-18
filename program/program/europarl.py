#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import re
from util import makeSeedList,statistic,writeStatisticResult,writeExtrateSentence

class SentencePair:
	def __init__(self,line):
		d = eval(line)
		info = d.values()[0]
		self.id = info['_id']
		self.align = info['align']
		self.wordEn = info['words1']
		self.wordGe = info['words2']
		self.alignEn = []
		for a in self.align:
			self.alignEn.append(a[1])
		self.alignGe = []
		for a in self.align:
			self.alignGe.append(a[0])
			
	def __eq__(self,other):
		return self.id==other.id

	def __hash__(self):
		return hash(self.id)
	
	# type: en->ge or ge->en
	def translationType(self,tType):
		if tType == "enToGe":
			sourceLanguage = self.wordEn
			sourceAlign = self.alignEn
			targetLanguage = self.wordGe
			targetAlign = self.alignGe
		else:
			sourceLanguage = self.wordGe
			sourceAlign = self.alignGe
			targetLanguage = self.wordEn
			targetAlign = self.alignEn
		return sourceLanguage,sourceAlign,targetLanguage,targetAlign
		
	
	def getTranslationStatistic(self,modalverb,countRes,sourceLanguage,sourceAlign,targetLanguage,targetAlign):
		for mv in modalverb:
			if mv in sourceLanguage:
				# find the index of modalverb
				sourceNos = [i for i, x in enumerate(sourceLanguage) if x == mv]
				# find correspond translation of modalverb through align
				for sNo in sourceNos:
					mvTransString = ""
					alis = [i for i, x in enumerate(sourceAlign) if x == sNo]
					for a in alis:
						targetNo = targetAlign[a]
						mvTransString += targetLanguage[targetNo] + " "
						statistic(countRes,mvTransString)
		return countRes
	
	def findSeedTranslation(self,modalverb,seed,sourceLanguage,sourceAlign,targetLanguage,targetAlign):
		translations = []
		modalV=""
		translationNo = 0
		modalNo = 0
		for mv in modalverb:
			if mv in sourceLanguage:
				sourceNos = [i for i, x in enumerate(sourceLanguage) if x == mv]
				for sNo in sourceNos:
					mvTransString = " "
					alis = [i for i, x in enumerate(sourceAlign) if x == sNo]
					for a in alis:
						targetNo = targetAlign[a]
						target = targetLanguage[targetNo]
						if target.lower() in seed:							
							mvTransString += targetLanguage[targetNo] + " " 
							translations.append(mvTransString)
							modalV = mv
							translationNo = targetNo
							modalNo = sNo
		return translations,modalV,translationNo,modalNo
	
		
	# -able -bar
	def findSpecialSeedTranslation(self,modalverb,seedCategory,sourceLanguage,sourceAlign,targetLanguage,targetAlign):
		translations = []
		modalV=""
		translationNo = 0
		modalNo = 0
		for mv in modalverb:
			if mv in sourceLanguage:
				# find the index of modalverb
				sourceNos = [i for i, x in enumerate(sourceLanguage) if x == mv]
				# find correspond translation of modalverb through align
				for sNo in sourceNos:
					mvTransString = " "
					alis = [i for i, x in enumerate(sourceAlign) if x == sNo]
					for a in alis:
						targetNo = targetAlign[a]
						target = targetLanguage[targetNo]
						for seed in seedCategory:
							if re.search(seed,target.lower()):
								mvTransString += targetLanguage[targetNo] + " "
								translations.append(mvTransString)
								modalV=mv
								translationNo = targetNo
								modalNo = sNo
		return translations,modalV,translationNo,modalNo
		
	def findSeedIndirect(self,modalverb1,modalverb2,seedCategory,sourceLanguage,sourceAlign,targetLanguage,targetAlign):
		modal1=""
		modal2=""
		seedContext=""
		d=0
		modal1No=0
		modal2No=0
		seedNo=0
		for mv1 in modalverb1:
			for seed in seedCategory:
				if mv1 in sourceLanguage and seed in targetLanguage:
					sourceNos = [i for i, x in enumerate(sourceLanguage) if x == mv1]
					for sNo in sourceNos:
						alis = [i for i, x in enumerate(sourceAlign) if x == sNo]
						#print alis
						for a in alis:
							targetNo = targetAlign[a]
							target = targetLanguage[targetNo]
							if target.lower() in modalverb2:
								modal2 = target
								modal1=mv1
								seedContext = seed
								d = targetLanguage.index(target) - targetLanguage.index(seed)
								modal1No=sNo
								modal2No=targetNo
								seedNo=targetLanguage.index(seed)
								#print modal1,modal2,seedContext
		return modal1,modal2,seedContext,d,modal1No,modal2No,seedNo
		
	def getSeedStatistic(self,modalverb,countRes,seedCategory,sourceLanguage,sourceAlign,targetLanguage,targetAlign):
		for mv in modalverb:
			if mv in sourceLanguage:
				# find the index of modalverb
				sourceNos = [i for i, x in enumerate(sourceLanguage) if x == mv]
				# find correspond translation of modalverb through align
				for sNo in sourceNos:
					mvTransString = ""
					alis = [i for i, x in enumerate(sourceAlign) if x == sNo]
					for a in alis:
						targetNo = targetAlign[a]
						target = targetLanguage[targetNo]
						if target.lower() in seedCategory:
							mvTransString += targetLanguage[targetNo] + " "
							statistic(countRes,mvTransString)
		return countRes
	
		
def extrateExcute(europarlFiles,tType,modalverbs,categoriesNormal,categoriesSpecial,fileNamesNormal,fileNamesSpecial):	
	writeFilesNormal = []
	for fileName in fileNamesNormal:
		writeFile = open(fileName,'w')
		writeFilesNormal.append(writeFile)
	
	writeFilesSpecial = []
	for fileName in fileNamesSpecial:
		writeFile = open(fileName,'w')
		writeFilesSpecial.append(writeFile)
	
	for europarlFile in europarlFiles:
		#spoSet = set([])
		f = open(europarlFile)
		lines = f.readlines()				
		for line in lines:
			spo = SentencePair(line)
			#spoSet.add(spo)		
		#for spo in spoSet:	
			typeInfo = spo.translationType(tType)
			sourceLanguage = typeInfo[0]
			sourceAlign = typeInfo[1]
			targetLanguage = typeInfo[2]
			targetAlign = typeInfo[3]		
			translationsAndMvsNormal=[]
			translationsAndMvsSpecial=[]
			for modalverb in modalverbs:
				for cate in categoriesNormal:
					translationsAndMvNormal = spo.findSeedTranslation(modalverb,cate,sourceLanguage,sourceAlign,targetLanguage,targetAlign)
					translationsAndMvsNormal.append(translationsAndMvNormal)
			for pair in zip(writeFilesNormal,translationsAndMvsNormal):
				writeExtrateSentence(pair[0],pair[1],spo)
			
			for modalverb in modalverbs:
				for cate in categoriesSpecial:
					translationsAndMvSpecial = spo.findSpecialSeedTranslation(modalverb,cate,sourceLanguage,sourceAlign,targetLanguage,targetAlign)
					translationsAndMvsSpecial.append(translationsAndMvSpecial)
			for pair in zip(writeFilesSpecial,translationsAndMvsSpecial):
				writeExtrateSentence(pair[0],pair[1],spo)		
	for f in writeFilesNormal:
		f.close()
	for f in writeFilesSpecial:
		f.close()
	
def contextExtrateExtute(europarlFiles,tType,modalverbs1,modalverbsTr,categories,fileNames):

	writeFiles = []
	for fileName in fileNames:
		writeFile = open(fileName,'w')
		writeFiles.append(writeFile)

	for europarlFile in europarlFiles:
		#spoSet = set([])
		f = open(europarlFile)
		lines = f.readlines()
		for line in lines:
			spo = SentencePair(line)
			#spoSet.add(spo)

		#for spo in spoSet:
			typeInfo = spo.translationType(tType)
			sourceLanguage = typeInfo[0]
			sourceAlign = typeInfo[1]
			targetLanguage = typeInfo[2]
			targetAlign = typeInfo[3]

			translationsAndMv1AndMv2AndDs = []

			for modalverb1 in modalverbs1:
				for cate in categories:
					translationsAndMv1AndMv2AndD = spo.findSeedIndirect(modalverb1,modalverbsTr,cate,sourceLanguage,sourceAlign,targetLanguage,targetAlign)
					translationsAndMv1AndMv2AndDs.append(translationsAndMv1AndMv2AndD)
			for pair in zip(writeFiles,translationsAndMv1AndMv2AndDs):
				if pair[1][3]!=0 and abs(pair[1][3])<=3:
					pair[0].write(str(spo.id)+'\n'+pair[1][0]+" "+pair[1][1]+" "+pair[1][2]+" "+str(pair[1][3])+'\n'+" ".join(spo.wordEn) + '\n'+" ".join(spo.wordGe)+'\n'+'\n')
		f.close()
		
def statisticExcute(europarlFiles,tType,modalverbs,seedCategory,fileNames):
	
	countResAll=[]
	
	for mv in modalverbs:
		for ca in seedCategory:
			countRes={}
			countResAll.append(countRes)
			
	#print len(countResAll)
	
	for europarlFile in europarlFiles:
		#spoSet = set([])
		f = open(europarlFile)
		lines = f.readlines()
		for line in lines:
			spo = SentencePair(line)
			#spoSet.add(spo)

		#for spo in spoSet:
			typeInfo = spo.translationType(tType)
			sourceLanguage = typeInfo[0]
			sourceAlign = typeInfo[1]
			targetLanguage = typeInfo[2]
			targetAlign = typeInfo[3]
			
			for i in range(len(modalverbs)+1)[1:]:
				for j in range(len(seedCategory)+1)[1:]:
					countResAll[j+len(seedCategory)*(i-1)-1] = spo.getSeedStatistic(modalverbs[i-1],countResAll[j+len(seedCategory)*(i-1)-1],seedCategory[j-1],sourceLanguage,sourceAlign,targetLanguage,targetAlign)
		f.close()
		
	for pair in zip(fileNames,countResAll):
		countResList = sorted(pair[1].iteritems(), key=lambda d:d[1], reverse = True)
		writeStatisticResult(pair[0],countResList)
		
def extrateAllInOneExcute(europarlFiles,tType,modalSeedList,writeFile):
	f = open(writeFile,'w')
	for europarlFile in europarlFiles:
		#spoSet = set([])
		f2 = open(europarlFile)
		lines = f2.readlines()
		for line in lines:
			spo = SentencePair(line)
			#spoSet.add(spo)
		#for spo in spoSet:	
			typeInfo = spo.translationType(tType)
			sourceLanguage = typeInfo[0]
			sourceAlign = typeInfo[1]
			targetLanguage = typeInfo[2]
			targetAlign = typeInfo[3]
			for pair in modalSeedList:
				translationsAndMv = spo.findSeedTranslation(pair[0],pair[1],sourceLanguage,sourceAlign,targetLanguage,targetAlign)
				writeExtrateSentence(f,translationsAndMv,spo)
	f.close()