import requests
from bs4 import BeautifulSoup

# open url and extact html object(soup)
def getSoup( url ):
    # html = urllib2.urlopen(url).read().encode('ascii','ignore')
    page = requests.get(url).text
    soup = BeautifulSoup(page, "lxml")
    return soup


# get links of a term as string type
def getTermLinks( letter ):
    termLinks = list()
    baseUrl = ('http://www.investopedia.com/terms/' + letter + '/')
    soup = getSoup(baseUrl)
    print("url: %s") % (baseUrl)

    # iterate each pages and store termLink into the list
    lastPage = soup.find("a", title="Go to last page")
    if lastPage == None:
        pageCount = 1
    else:
        pageCount = int(lastPage.get("href").lstrip("terms/" + letter + "?page="))

    for pageNum in xrange(1,pageCount+1):
        if pageNum != 1:
            #(e.g)http://www.investopedia.com/terms/a/?page=13 for term 'A'
            pageUrl = ('http://www.investopedia.com/terms/' + letter + '/?page=' + str(pageNum))
            soup = getSoup(pageUrl)
            # print("url: %s") % (pageUrl)
            print("."),
        
        # links stores relative term url (e.g) "term/a/abend.asp"
        links = soup.find("div", class_="box col-2 big-item-title clear").find_all("a")
        for link in links:
            termLinks.append(link.get("href"))

    print "%d links fetched\n" % (len(termLinks))
    return termLinks
