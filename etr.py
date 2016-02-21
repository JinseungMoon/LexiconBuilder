import requests
from bs4 import BeautifulSoup

# open url and extact html object(soup)
def getSoup( url ):
    # html = urllib2.urlopen(url).read().encode('ascii','ignore')
    page = requests.get(url).text
    soup = BeautifulSoup(page, "lxml")
    return soup


# get herf content only from a <a> tag
def getHrefs( elements, tag, classAtr):
    links = list()
    linkElements = elements.find(tag, class_=classAtr).find_all("a")
    for linkElment in linkElements:
        links.append(linkElment.get("href"))
    return links


# get links of a term as string type
def getTermLinks( letter ):
    baseUrl = ('http://www.investopedia.com/terms/' + letter + '/')
    pageContent = getSoup(baseUrl).body.find("div", class_="layout-page")
    print("url: %s") % (baseUrl)

    termLinks = list()
    
    # iterate each pages and store termLink into the list
    lastPage = pageContent.find("a", title="Go to last page")
    if lastPage == None:
        pageCount = 1
    else:
        pageCount = int(lastPage.get("href").lstrip("terms/" + letter + "?page="))

    for pageNum in xrange(1,pageCount+1):
        if pageNum != 1:
            #(e.g)http://www.investopedia.com/terms/a/?page=13 for term 'A'
            pageUrl = ('http://www.investopedia.com/terms/' + letter + '/?page=' + str(pageNum))
            pageContent = getSoup(pageUrl).body.find("div", class_="layout-page")
            # print("url: %s") % (pageUrl)
            print("."),
        
        # links stores relative term url (e.g) "term/a/abend.asp"
        termLinks += getHrefs(pageContent, "div", "box col-2 big-item-title clear")
    
    print "%d links fetched\n" % (len(termLinks))
    return termLinks
