#!/usr/bin/python
# -*- coding: utf-8 -*-

from europarl import *
from util import *
from findMorePara import *


"""
Extrate labeled Data, using English paraphrases to extrate labeled German modal verb.
"""

europarlFiles = ['../EPOS/en-de.pos-pts.txt','../EPOS/DE_intersect00.txt', '../EPOS/DE_intersect01.txt']
#europarlFiles = ['../EPOS/test.txt']

engSeeds = getEngSeedsList()

koennen = ['kann','kannst','können','könnt','konnte','konntest','konnten','konntet','könne','könnest','könnet','könnte','könntest','könnten','könntet','gekonnt','könnend','Kann','Kannst','Können','Könnt','Konnte','Konntest','Konnten','Konntet','Könne','Könnest','Könnet','Könnte','Könntest','Könnten','Könntet','Gekonnt','Könnend']
muessen = ['muss','musst','müssen','müsst','musste','musstest','mussten','musstet','müsse','müssest','müsset','müsste','müsstest','müssten','müsstet','gemusst','müssend','muß','mußt','müßen','müßt','mußte','mußtest','mußten','mußtet','müße','müßest','müßet','müßte','müßtest','müßten','müßtet','gemußt','müßend','Muss','Musst','Müssen','Müsst','Musste','Musstest','Mussten','Musstet','Müsse','Müssest','Müsset','Müsste','Müsstest','Müssten','Müsstet','Gemusst','Müssend','Muß','Mußt','Müßen','Müßt','Mußte','Mußtest','Mußten','Mußtet','Müße','Müßest','Müßet','Müßte','Müßtest','Müßten','Müßtet','Gemußt','Müßend']
sollen = ['soll','sollst','sollen','sollt','sollte','solltest','sollten','solltet','solle','sollest','sollet','sollte','solltest','sollten','gesollt','Soll','Sollst','Sollen','Sollt','Sollte','Solltest','Sollten','Solltet','Solle','Sollest','Sollet','Sollte','Solltest','Sollten','Gesollt']
duerfen = ['darf','darfst','dürfen','dürft','durfte','durftest','durften','durftet','dürfe','dürfest','dürfet','dürfte','dürftest','dürften','dürftet','gedurft','Darf','Darfst','Dürfen','Dürft','Durfte','Durftest','Durften','Durftet','Dürfe','Dürfest','Dürfet','Dürfte','Dürftest','Dürften','Dürftet','Gedurft']

moegen = ['mag', 'möge', 'mögen', 'mögt', 'magst', 'mögest', 'möget']
moechten = ['mochte', 'mochtest', 'mochten', 'mochtet', 'möchte', 'möchtest', 'möchten', 'möchtet']


#germanModal = [koennen,muessen,sollen,duerfen]
#germanModal = [moegen,moechten]

koennenKonjunktive = ['könnte','könnten','könne']
koennenIndicative = ['kann','können']

duerfenKonjunktive = ['dürfte','dürften']
sollenKonjunktive = ['sollte']

moegenCheck = ['mag','mögen']

germanModal = [koennenKonjunktive, duerfenKonjunktive, sollenKonjunktive, moegenCheck]

might = ['might','Might']

modalMightList = [(koennenKonjunktive,might),(duerfenKonjunktive,might),(sollenKonjunktive,might),(moegenCheck,might)]

#print "modalMightList: "+ str(modalMightList)


# orignal seeds extraction for more than 80 English seeds

"""
modalSeedList = []

for engSeed in engSeeds:

    for para in engSeed:
        upperLower = []
        upperLower.append(para)
        upperLower.append(para[0].upper()+para[1:len(para)])

        for gm in germanModal:
            modalSeedList.append((gm,upperLower))

print modalSeedList
print len(modalSeedList)
"""

if __name__ == '__main__':

    #extrateAllInOneExcute(europarlFiles,"goToEn",modalSeedList,"germanModalData_moegen.txt")

    extrateAllInOneExcute(europarlFiles,"goToEn",modalMightList,"germanModalData_might.txt")


