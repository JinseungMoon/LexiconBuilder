# -*- coding: utf-8 -*-
import etr
import string

idxList = str('1') + string.lowercase[:26] # 1 for #
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
        print "\n\n----------------------------------------------------------------"
        print "%s" % (termUrl)
        print "----------------------------------------------------------------"

         # extract definition and break down of term
        termContentElements = etr.getSoup(termUrl).find("div", id="Content") # element of id="Content"
        termDefElement = termContentElements.find("div", class_="content-box content-box-term").p 

        print "[Definition]"
        print repr(termDefElement.text)

        print "\n[Break Down]"
        print repr(termDefElement.find_next_siblings('p')[0].text)

        print "\n[Links]"
        relatedLinks = etr.getHrefs(termContentElements, "div", "box below-box col-2 no-image gray clear")
        for link in relatedLinks:
            print link

        termCount += len(termLinks)

    print ("total number pages from alphabet '%s' = %d\n") % (idxList[i], termCount)


print "total number of pages extracted = %d" % totalCount


