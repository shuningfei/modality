from tranStat import *
from findMorePara import *
from extrateLabelData import *

#tengSeeds = getEngSeedsList()

def formatChange():

    outputInstList = []

    f = open('extrateData/englishModalData.txt')

    instances = f.read().split('\n\n')

    for inst in instances:

        instEles = inst.split('\n')

        #print instEles

        modal = instEles[1].split(' ')[0]
        modalIndex = instEles[1].split(' ')[2]
        sent = instEles[2]
        seed = instEles[1].split(' ')[1]

        #print modal
        #print modalIndex
        #print sent
        #print seed

        #print

        label = ''

        for eles in seedsGeEp:
            for ele in eles:
                if ele==seed.lower():
                    label = 'ep'

        for eles in seedsGeDe:
            for ele in eles:
                if ele==seed.lower():
                    label = 'de'

        for eles in seedsGeDy:
            for ele in eles:
                if ele==seed.lower():
                    label = 'dy'

        oneInst = sent + '\t' + modal + '\t' + modalIndex + '\t' + label

        outputInstList.append(oneInst)

        outputInstList = list(set(outputInstList))

    return outputInstList

def writeData():

    fw_can = open('extrateData/enModalData/can.txt','w')
    fw_could = open('extrateData/enModalData/could.txt','w')
    fw_should = open('extrateData/enModalData/should.txt','w')
    fw_shall = open('extrateData/enModalData/shall.txt','w')
    fw_must = open('extrateData/enModalData/must.txt','w')
    fw_may = open('extrateData/enModalData/may.txt','w')

    instances = formatChange()

    for inst in instances:
        eles = inst.split('\t')

        modal = eles[1]
        if modal.lower()=='can':
            fw_can.write(eles[0]+'\t'+eles[2]+'\t'+eles[3]+'\n')

        if modal.lower()=='could':
            fw_could.write(eles[0]+'\t'+eles[2]+'\t'+eles[3]+'\n')

        if modal.lower()=='may':
            fw_may.write(eles[0]+'\t'+eles[2]+'\t'+eles[3]+'\n')

        if modal.lower()=='must':
            fw_must.write(eles[0]+'\t'+eles[2]+'\t'+eles[3]+'\n')

        if modal.lower()=='should':
            fw_should.write(eles[0]+'\t'+eles[2]+'\t'+eles[3]+'\n')

        if modal.lower()=='shall':
            fw_shall.write(eles[0]+'\t'+eles[2]+'\t'+eles[3]+'\n')

def formatChangeGe():

    engSeeds = getEngSeedsList()

    seedsEnEp = engSeeds[0]
    seedsEnDe = engSeeds[1]
    seedsEnDy = engSeeds[2]

    #print seedsEnEp
    #print seedsEnDe
    #print seedsEnDy

    outputInstList = []

    f = open('extrateData/germanModalData.txt')

    instances = f.read().split('\n\n')

    for inst in instances:

        instEles = inst.split('\n')

        #print instEles

        modal = instEles[1].split(' ')[0]
        modalIndex = instEles[1].split(' ')[2]
        sent = instEles[3]
        seed = instEles[1].split(' ')[1]

        #print modal
        #print modalIndex
        #print sent
        #print seed

        #print

        label = ''

        if seed.lower() in seedsEnEp:
            label = 'ep'

        if seed.lower() in seedsEnDe:
            label = 'de'

        if seed.lower() in seedsEnDy:
            label = 'dy'

        oneInst = sent + '\t' + modal + '\t' + modalIndex + '\t' + label

        outputInstList.append(oneInst)

        outputInstList = list(set(outputInstList))

    print outputInstList
    print len(outputInstList)

    return outputInstList

def writeDataGe():

    #print "HIIIIIII"


    fw_koennen = open('extrateData/geModalData/koennen.txt','w')
    fw_muessen = open('extrateData/geModalData/muessen.txt','w')
    fw_sollen = open('extrateData/geModalData/sollen.txt','w')
    fw_duerfen = open('extrateData/geModalData/duerfen.txt','w')



    instances = formatChangeGe()

    for inst in instances:
        eles = inst.split('\t')

        modal = eles[1]
        if modal.lower() in koennen:
            fw_koennen.write(eles[0]+'\t'+eles[2]+'\t'+eles[3]+'\n')

        if modal.lower() in muessen:
            fw_muessen.write(eles[0]+'\t'+eles[2]+'\t'+eles[3]+'\n')

        if modal.lower() in sollen:
            fw_sollen.write(eles[0]+'\t'+eles[2]+'\t'+eles[3]+'\n')

        if modal.lower() in duerfen:
            fw_duerfen.write(eles[0]+'\t'+eles[2]+'\t'+eles[3]+'\n')



if __name__ == '__main__':

    #formatChange()

    #writeData()

    #formatChangeGe()

    writeDataGe()


