import pickle
from europarl import *
from util import *
import sys

"""
calculate p(e' | e) = sum_f  p(f | e) x p(e' | f)

"""
europarlFiles = ['../EPOS/en-de.pos-pts.txt','../EPOS/DE_intersect00.txt', '../EPOS/DE_intersect01.txt']
#europarlFiles = ['../EPOS/test.txt']

labels = ['ep','de','dy']

# Get English seeds: ep, de, dy
def getEngSeedsList():

    f = open('Eng_seeds_end.txt')
    gSeeds = f.read().split('\n\n')
    eSeeds_epAll = []
    eSeeds_deAll = []
    eSeeds_dyAll = []

    for gSeed_ep in gSeeds[:11]:
        eSeeds_ep = gSeed_ep.split('\n')[1:]
        eSeeds_epAll.extend(eSeeds_ep)

    for gSeed_de in gSeeds[11:21]:
        eSeeds_de = gSeed_de.split('\n')[1:]
        eSeeds_deAll.extend(eSeeds_de)

    for gSeed_dy in gSeeds[21:]:
        eSeeds_dy = gSeed_dy.split('\n')[1:]
        eSeeds_dyAll.extend(eSeeds_dy)

    eSeeds_epAllBetter = []
    eSeeds_deAllBetter = []
    eSeeds_dyAllBetter = []

    for e in eSeeds_epAll:
        eSeeds_epAllBetter.append(e.strip())
    for e in eSeeds_deAll:
        eSeeds_deAllBetter.append(e.strip())
    for e in eSeeds_dyAll:
        eSeeds_dyAllBetter.append(e.strip())

    eSeeds_epAllBetter = sorted(list(set(eSeeds_epAllBetter)))
    eSeeds_deAllBetter = sorted(list(set(eSeeds_deAllBetter)))
    eSeeds_dyAllBetter = sorted(list(set(eSeeds_dyAllBetter)))


    #print len(eSeeds_epAllBetter)
    #print len(eSeeds_deAllBetter)
    #print len(eSeeds_dyAllBetter)

    return eSeeds_epAllBetter,eSeeds_deAllBetter,eSeeds_dyAllBetter

# aim is to calculate p(f|e), f - any german paraphrases, e - english seeds

def calculateFE():
    engSeeds = getEngSeedsList()
    print len(engSeeds)

    for pair in zip(engSeeds,labels):

        countResAll = []
        allSeeds = []
        for para in pair[0]:
            countRes = {}
            upperLower = []
            upperLower.append(para)
            upperLower.append(para[0].upper()+para[1:len(para)])

            allSeeds.append(upperLower)
            countResAll.append(countRes)

        #print allSeeds
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

            for i in range(len(allSeeds)):
                countResAll[i] = spo.getTranslationStatistic(allSeeds[i],countResAll[i],sourceLanguage,sourceAlign,targetLanguage,targetAlign)

        output = open('GermanParaList/germanPara_'+pair[1]+'.pkl', 'w')

        #print zip(allPara,countResAll)
        pickle.dump(zip(allSeeds,countResAll),output)



def getProbabilityFE(flag):

    germanParaListFile = open('GermanParaList/germanPara_'+flag+'.pkl','r')

    germanParaList = pickle.load(germanParaListFile)

    for seed in germanParaList:

        prob = []

        prob.append(seed[0])

        prob.append(convertCountToProbabilitySorted(seed[1]))

        print prob

# aim is to calculate p(e'|f), f - any german paraphrases, e' - any Eng paraphrases

def getGermanForeignList(flag):
    germanParaListFile = open('GermanParaList/germanPara_'+flag+'.pkl','r')

    germanParaList = pickle.load(germanParaListFile)

    for seed in germanParaList:

        #print seed[0][0]

        countResAll = []
        allSeeds = []

        sorted = sortCountList(seed[1])

        for para in sorted:

            gerPara = para[0].strip()

            countRes = {}
            upperLower = []
            upperLower.append(gerPara)
            upperLower.append(gerPara[0].upper()+gerPara[1:len(gerPara)])

            allSeeds.append(upperLower)
            countResAll.append(countRes)

        #print allSeeds
        #print countResAll

        for europarlFile in europarlFiles:
            f = open(europarlFile)
            lines = f.readlines()

        for line in lines:

            spo = SentencePair(line)
            typeInfo = spo.translationType('geToEn')
            sourceLanguage = typeInfo[0]
            sourceAlign = typeInfo[1]
            targetLanguage = typeInfo[2]
            targetAlign = typeInfo[3]

            for i in range(len(allSeeds)):

                countResAll[i] = spo.getTranslationStatistic(allSeeds[i],countResAll[i],sourceLanguage,sourceAlign,targetLanguage,targetAlign)

        output = open('EngParaList/engPara_'+flag+'_'+seed[0][0]+'.pkl', 'w')

        #print zip(allPara,countResAll)
        pickle.dump(zip(allSeeds,countResAll),output)

def getProbabilityFEE2F(flag, constraint_value, product_contraint):


    germanParaListFile = open('GermanParaList/germanPara_'+flag+'.pkl','r')

    germanParaList = pickle.load(germanParaListFile)


    for j in range(len(germanParaList)):

        goodSeeds =[]

        print "Gold seed: " + germanParaList[j][0][0]

        engParaListFile = open('EngParaList/engPara_'+flag+'_'+germanParaList[j][0][0]+'.pkl','r')

        engParaList = pickle.load(engParaListFile)

        elesAll = []

        engSeedsAll = []

        for i in range(len(engParaList)):

            probabilityListEng = convertCountToProbabilitySorted(engParaList[i][1])

            for oneEseed in probabilityListEng:

                eles = []
                p_e2_f = oneEseed[1]

                probabilityGe = convertCountToProbabilitySorted(germanParaList[j][1])[i]
                p_f_e = probabilityGe[1]

                p_f_e_Mul_p_e2_f = p_f_e * p_e2_f

                eles.append(oneEseed[0])
                eles.append(probabilityGe[0])
                eles.append(p_f_e_Mul_p_e2_f)

                elesAll.append(eles)
                engSeedsAll.append(oneEseed[0])

        engSeedsAll = list(set(engSeedsAll))

        for engSeed in engSeedsAll:

            #print "engSeed: " + engSeed

            sum_f = 0
            for eles in elesAll:
                if eles[0]==engSeed:
                    sum_f+=float(eles[2])
            if sum_f > float(constraint_value) and eles[2] > float(product_contraint):
                goodSeeds.append(engSeed)

                #print "sum_f: " + str(sum_f)
                #print "eles2: " + str(eles[2])

        goodSeeds = list(set(goodSeeds))


        #goodSeeds = list(set(goodSeeds))
        #print
        print "seeds exceed threshold for this gold seed: "
        print goodSeeds
        print "totally number: " + str(len(goodSeeds))
        print

def getProbabilityFEE2FOneIteration(flag):

    goodSeeds =[]

    germanParaListFile = open('GermanParaList/germanPara_'+flag+'.pkl','r')

    germanParaList = pickle.load(germanParaListFile)

    engParaListFile = open('EngParaList/engPara_ep_apparently.pkl','r')

    engParaList = pickle.load(engParaListFile)


    elesAll = []

    engSeedsAll = []


    for i in range(len(engParaList)):

        #print eSeed[0][0]
        #print "Geee: " + engParaList[i][0][0]

        #print convertCountToProbabilitySorted(eSeed[1])

        probabilityListEng = convertCountToProbabilitySorted(engParaList[i][1])

        #print len(probabilityListEng)

        for oneEseed in probabilityListEng:

            eles = []

            #print oneEseed[0]
            p_e2_f = oneEseed[1]
            #print p_e2_f

            #print germanParaList[0][0]
            probabilityGe = convertCountToProbabilitySorted(germanParaList[0][1])[i]
            #print probabilityGe[0]
            p_f_e = probabilityGe[1]
            #print p_f_e

            p_f_e_Mul_p_e2_f = p_f_e * p_e2_f

            eles.append(oneEseed[0])
            eles.append(probabilityGe[0])
            eles.append(p_f_e_Mul_p_e2_f)

            elesAll.append(eles)
            engSeedsAll.append(oneEseed[0])

    engSeedsAll = list(set(engSeedsAll))

    for engSeed in engSeedsAll:

        #print "engSeed: " + engSeed

        sum_f = 0
        for eles in elesAll:
            if eles[0]==engSeed:
                sum_f+=float(eles[2])
        if sum_f > float(constraint_value) and eles[2] > float(product_contraint):
            goodSeeds.append(engSeed)

            #print "sum_f: " + str(sum_f)
            #print "eles2: " + str(eles[2])

    goodSeeds = list(set(goodSeeds))

    """
    for eles in elesAll:
        sum_f = 0
        for engSeed in engSeedsAll:
            if eles[0]==engSeed:

                print "eles[0]: " + eles[0]
                print "engSeed: " + engSeed

                sum_f+=float(eles[2])

                print "sum_f: " + str(sum_f)
                print "eles2: " + str(eles[2])

        if sum_f > 0.009:
            goodSeeds.append(eles[0])

    goodSeeds = list(set(goodSeeds))
    """
    print goodSeeds
    print len(goodSeeds)


def lookme(flag):

    germanParaListFile = open('GermanParaList/germanPara_'+flag+'.pkl','r')

    germanParaList = pickle.load(germanParaListFile)

    engParaListFile = open('EngParaList/engPara_ep_apparently.pkl','r')

    engParaList = pickle.load(engParaListFile)

    for eSeed in engParaList:

        eProb = []

        eProb.append(eSeed[0])

        eProb.append(convertCountToProbabilitySorted(eSeed[1]))

        print eProb

    print

    for gSeed in germanParaList:

        gProb = []

        gProb.append(gSeed[0])

        gProb.append(convertCountToProbabilitySorted(gSeed[1]))

        print gProb





if __name__ == '__main__':

    #getEngSeedsList()
    #calculateFE()

    #getProbabilityFE('ep')


    #for la in labels:
        #getGermanForeignList(la)

    #lookme('ep')

    #getProbabilityFEE2FOneIteration('ep')



    try:
        getProbabilityFEE2F(sys.argv[1],sys.argv[2],sys.argv[3])
    except IndexError:
        print "***************"
        print "Please give modal category and threshold value as arguments !!!"
        print "Usage: python findMorePara.py [category] [sum_threshold] [product_threshold]"
        print "Example: python findMorePara.py ep 0.009 0.000001"
        print "***************"
