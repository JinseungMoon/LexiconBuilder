# -*- coding: utf-8 -*-
import os
import codecs
import requests
import json
import Queue
import threading
from bs4 import BeautifulSoup
from datetime import datetime

# -----------------------------------------------------------------------------------
# ------------Global variables
# -----------------------------------------------------------------------------------
baseUrl = "http://www.investopedia.com"
# letterList = '1abcdefghijklmnopqrstuvwxyz'
letterList = 'd'
lock = threading.Lock()
dictionary = list()
urlTree = []
termTree = []
fetchedCount = 0
###########https://docs.python.org/2/howto/logging.html

# -----------------------------------------------------------------------------------
# ------------Functions
# -----------------------------------------------------------------c------------------
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
        
        # links stores relative term url (e.g) "term/a/abend.asp"
        links = soup.find("div", class_="box col-2 big-item-title clear").find_all("a")
        
        for link in links:
            termLinks.append(link.get("href"))

    print "%s '%d' links fetched." % (baseUrl, len(termLinks))
    
    global fetchedCount
    with lock:
    	fetchedCount += len(termLinks)

    dictionary.append(termLinks)

    return fetchedCount

def extractContent(idx):
    for termLink in dictionary[idx]:

        termLeaf = {}

        termUrl = baseUrl + termLink
        # termUrl = "http://www.investopedia.com/terms/c/cesar-alierta-izuel.asp"

        # extract definition and break down of term
        soup = getSoup(termUrl)

        content = soup.find("div", class_="content-box content-box-term")

        if content == None:
        	continue

        term = soup.h1.text.strip()
        termLeaf['term'] = term
        termLeaf['url'] = termUrl
        urlTree.append({'term' : term, 'url' : termUrl})
        print repr(term) + '\t' + repr(termUrl)

        tags = content.find_all(['h2','p'])

        definition = ''
        breakdown = ''
        anchorTerms = []
        for tag in tags:
        	if tag.name == 'p':
				if tag == tags[1]:
					definition += ''.join(tag.text)
				else:
					breakdown += ''.join(tag.text)
				anchorTermElements = tag.find_all('a')
				for element in anchorTermElements:
					anchorTerms.append({'term': element.text.strip(), 'url': "http://www.investopedia.com" + element['href']})
		termLeaf['definition'] = definition.strip()
		termLeaf['breakdown'] = breakdown.strip()
        termLeaf['anchorTerms'] = anchorTerms


        	
        # extract related links
        relatedTerms = []

    	relatedTermElements = soup.find("div", class_="box below-box col-2 no-image gray clear").find_all("a")
    	for element in relatedTermElements:
    	    relatedTerms.append({'term': element.contents[0].strip(), 'url': "http://www.investopedia.com" + element['href']})


        termLeaf['relatedTerms'] = relatedTerms

        with lock:
        	termTree.append(termLeaf)

        sleep(1)	

			
def worker():
    while True:
        letter = q.get()
        fetchedCount = getTermLinks(letter)
        q.task_done()

def worker2():
    while True:
        index = q2.get()
        extractContent(index)
        q2.task_done()


# -----------------------------------------------------------------------------------
# ---------------- main
# -----------------------------------------------------------------------------------
q = Queue.Queue()
q2 = Queue.Queue()
num_worker_threads = 26
# logf = codecs.open(outDir + 'log.txt', encoding='utf-8', mode='wa')

for i in range(num_worker_threads):
     t = threading.Thread(target=worker)
     t.daemon = True
     t.start()

for letter in letterList:
    q.put(letter)

q.join() 


print "all links are fetched.\n"
for i in range(num_worker_threads):
	t = threading.Thread(target=worker2)
	t.demon = True
	t.start()

for i in xrange(len(dictionary)):
	q2.put(i)

q2.join()

print "all contents are fetched.\n"
# dump data to json files
os.chdir("../")

# write url list
furl = codecs.open('out/urlList.json', encoding='utf-8', mode='w+b')
json.dump(urlTree, furl)
furl.close()	


# write term data
fterm = codecs.open('out/term.json', encoding='utf-8', mode='w+b')
json.dump(termTree, fterm)
fterm.close()


# print out result
print "\n# of fetched Pages: %d" % fetchedCount