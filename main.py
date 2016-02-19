# -*- coding: utf-8 -*-
import etr
import string
import os

idxList = str('1') + string.lowercase[:26] # 1 for #
#idxList = str('1')
termLinks = list()


# extract links from each letter("#~Z")
for termIdx in idxList:
    termLinks.append(etr.getTermLinks(termIdx))


# print all data
totalCount = 0
for i in xrange(len(idxList)):
    termCount = 0

    for termLink in termLinks[i]:

        termUrl = ("http://www.investopedia.com"+ termLink)
        print "\n\n--------------------------------------------------------------------------------"
        print "%s" % (termUrl)
        print "--------------------------------------------------------------------------------"

         # extract definition and break down of term
        termContentElements = etr.getSoup(termUrl).find("div", id="Content") # element of id="Content"
        termDefElement = termContentElements.find("div", class_="content-box content-box-term").p 

        # write on a txt file
        curDir = os.getcwd()
        filePath = curDir + "/data" + termLink.lstrip("terms").rstrip(".asp") + ".txt"
        linkfilePath = filePath.rstrip(".txt") + "_RT.txt"
       
        targetDir = os.path.dirname(filePath)
        if not os.path.exists(targetDir):
            os.makedirs(targetDir)
        
        f = open(filePath, 'w')
        fl = open(linkfilePath, 'w')
       
        f.write("[Definition]\n")
        f.write(termDefElement.text.encode('utf-8'))

        f.write("\n\n[Break Down]\n")
        f.write(termDefElement.find_next_siblings('p')[0].text.encode('utf-8'))

        # print "\n[Links]"
        relatedLinks = etr.getHrefs(termContentElements, "div", "box below-box col-2 no-image gray clear")
        for link in relatedLinks:
            # print link
            fl.write(link + '\n')

        termCount += len(termLinks)
        f.close()
        fl.close()
        print '\'' + filePath + '\'' + ' completed'
        print '\'' + linkfilePath + '\''+ ' completed'

    print ("total number pages from alphabet '%s' = %d\n") % (idxList[i], termCount)


print "total number of pages extracted = %d" % totalCount


