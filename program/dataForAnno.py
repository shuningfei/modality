from tranStat import *
from findMorePara import *
from extrateLabelData import *
import random

def dataForAnno():

    engSeeds = getEngSeedsList()

    seedsEnEp = engSeeds[0]
    seedsEnDe = engSeeds[1]
    seedsEnDy = engSeeds[2]

    outputInstList = []

    f = open('extrateData/germanModalData_moegen.txt')

    instances = f.read().split('\n\n')

    for inst in instances:

        instEles = inst.split('\n')

        #print instEles

        modal = instEles[1].split(' ')[0]
        modalIndex = instEles[1].split(' ')[2]
        seedIndex = instEles[1].split(' ')[3]
        sent = instEles[3]
        seed = instEles[1].split(' ')[1]

        engSent = instEles[2]

        label = ''

        if seed.lower() in seedsEnEp:
            label = 'ep'

        if seed.lower() in seedsEnDe:
            label = 'de'

        if seed.lower() in seedsEnDy:
            label = 'dy'

        oneInst = sent + '\t' + modal + '\t' + modalIndex + '\t' + label + '\t' + seed + '\t' + engSent + '\t' + seedIndex

        outputInstList.append(oneInst)

        outputInstList = list(set(outputInstList))

    print outputInstList
    print len(outputInstList)

    return outputInstList

def writeDataGe():

    engSeeds = getEngSeedsList()

    instances = dataForAnno()

    random.shuffle(instances)

    engSeedsAll = []

    seedsEnEp = engSeeds[0]
    seedsEnDe = engSeeds[1]
    seedsEnDy = engSeeds[2]

    engSeedsAll.extend(seedsEnEp)
    engSeedsAll.extend(seedsEnDe)
    engSeedsAll.extend(seedsEnDy)

    #print engSeedsAll

    for seed in engSeedsAll:

        for cate in ['ep','de','dy']:

            """
            fw_koennen = open('extrateData/geModalData/koennen/'+cate+'/'+seed+'.txt','w')
            fw_muessen = open('extrateData/geModalData/muessen/'+cate+'/'+seed+'.txt','w')
            fw_sollen = open('extrateData/geModalData/sollen/'+cate+'/'+seed+'.txt','w')
            fw_duerfen = open('extrateData/geModalData/duerfen/'+cate+'/'+seed+'.txt','w')
            """

            fw_moegen = open('extrateData/geModalData/moegen/'+cate+'/'+seed+'.txt','w')
            fw_moechten = open('extrateData/geModalData/moechten/'+cate+'/'+seed+'.txt','w')

            for inst in instances:
                eles = inst.split('\t')

                modal = eles[1]
                thisSeed = eles[4]
                label = eles[3]

                """
                if modal.lower() in koennen and seed==thisSeed and cate==label:
                    fw_koennen.write(eles[0]+'\t'+eles[2]+'\t'+eles[3]+'\n')
                    fw_koennen.write(eles[5]+'\t'+eles[6]+'\n\n')

                if modal.lower() in muessen and seed==thisSeed and cate==label:
                    fw_muessen.write(eles[0]+'\t'+eles[2]+'\t'+eles[3]+'\n')
                    fw_muessen.write(eles[5]+'\t'+eles[6]+'\n\n')

                if modal.lower() in sollen and seed==thisSeed and cate==label:
                    fw_sollen.write(eles[0]+'\t'+eles[2]+'\t'+eles[3]+'\n')
                    fw_sollen.write(eles[5]+'\t'+eles[6]+'\n\n')

                if modal.lower() in duerfen and seed==thisSeed and cate==label:
                    fw_duerfen.write(eles[0]+'\t'+eles[2]+'\t'+eles[3]+'\n')
                    fw_duerfen.write(eles[5]+'\t'+eles[6]+'\n\n')
                """

                if modal.lower() in moegen and seed==thisSeed and cate==label:
                    fw_moegen.write(eles[0]+'\t'+eles[2]+'\t'+eles[3]+'\n')
                    fw_moegen.write(eles[5]+'\t'+eles[6]+'\n\n')

                if modal.lower() in moechten and seed==thisSeed and cate==label:
                    fw_moechten.write(eles[0]+'\t'+eles[2]+'\t'+eles[3]+'\n')
                    fw_moechten.write(eles[5]+'\t'+eles[6]+'\n\n')


if __name__ == '__main__':
    writeDataGe()

