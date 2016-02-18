# -*- coding: utf-8 -*-
import urllib2
from bs4 import BeautifulSoup

# function :
# open url and extact html object(soup)
def extSoup( url ):
    html = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html, "lxml")
    return soup

# extract list of terms
termIdx = 'a'
baseUrl = ('http://www.investopedia.com/terms/' + termIdx + '/')
pageContent = extSoup(baseUrl).body.find("div", class_="layout-page")
print("url: %s") % (baseUrl)

# iterate each pages and store termLink into the list
totalCountOfTerm = 0
termLinkList = list()
pageCount = int(pageContent.find("a", title="Go to last page").get("href").lstrip("terms/" + termIdx + "?page="))

for pageNum in xrange(1,2):
    if pageNum != 1:
        #(e.g)http://www.investopedia.com/terms/a/?page=13 for term 'A'
        pageUrl = ('http://www.investopedia.com/terms/' + termIdx + '/?page=' + str(pageNum))
        pageContent = extSoup(pageUrl).body.find("div", class_="layout-page")
        print("url: %s") % (pageUrl)
    
    # termLinkList stores relative term url (e.g) "term/a/abend.asp"
    termLinkTagList = pageContent.find("div", class_="box col-2 big-item-title clear").find_all("a")
    for termLinkTag in termLinkTagList:
        termLinkList.append(termLinkTag.get("href"))

    print len(termLinkList)    
    totalCountOfTerm += len(termLinkList)

print ("total number of term '%s' = %d\n") % (termIdx, totalCountOfTerm)

# for termLink in termLinkList:

#     termUrl = ("http://www.investopedia.com"+ termLink + '.asp')
#     print "\n\n----------------------------------------------------------------"
#     print "[%s] from (%s)" % (termLink, termUrl)
#     print "----------------------------------------------------------------"

#      # extract definition and break down of term
#     termContent = extSoup(termUrl).find("div", class_="content-box content-box-term").p

#     print "[Definition]"
#     print termContent.text

#     print "\n[Break Down]"
#     print "%s\n" % (termContent.find_next_siblings('p')[0].text)

#     # extract links of term
#     print "[Links]"
#     linkList = termSoup.find("div", class_="box below-box col-2 no-image gray clear").find_all("a")
#     for link in linkList:
#         print(link.get("href"))
