# -*- coding: utf-8 -*-
import os
import codecs
import requests
import Queue
import threading
from multiprocessing.dummy import Pool as ThreadPool
import time
from bs4 import BeautifulSoup
from datetime import datetime

# -----------------------------------------------------------------------------------
# ------------Global values
# -----------------------------------------------------------------------------------
baseUrl = "http://www.investopedia.com"
letterList = '1abcdefghijklmnopqrstuvwxyz'
#letterList = 'defg1qrz'
outDir = os.getcwd() + "/out/"
lock = threading.Lock()
dictionary = list()
totalCount = 0
warnCount = 0


# -----------------------------------------------------------------------------------
# ------------Functions
# -----------------------------------------------------------------------------------
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

    print "%s '%d' links fetched.\n" % (baseUrl, len(termLinks))
    dictionary.append(termLinks)

def extractContent(idx):
 	for termLink in dictionary[idx]:

		termUrl = baseUrl + termLink
		#termUrl = "http://www.investopedia.com/terms/p/ppipla.asp"
		
		print "%s" % (termUrl) 

		# write on a txt file
		filePath = outDir + termUrl[len(baseUrl)+1:].rstrip(".asp") + ".txt"
		linkfilePath = filePath.rstrip(".txt") + "_RT.txt"

		targetDir = os.path.dirname(filePath)
		if not os.path.exists(targetDir):
		    os.makedirs(targetDir)

		f = codecs.open(filePath, encoding='utf-8', mode='w')
		fl = codecs.open(linkfilePath, encoding='utf-8', mode='w')


		 # extract definition and break down of term
		soup = getSoup(termUrl)

		content = soup.find("div", class_="content-box content-box-term")

		if content == None:
			logf.write(str('[Invalid Format#1!]' + termLink + '\n'))
			f.close()
			fl.close()
			continue

		termDefElements = content.find_all('p') 

		if len(termDefElements) <= 1:
			logf.write(str('[Invalid Format#2!]' + termLink + '\n'))
			with lock:
				global warnCount
				warnCount += 1

		for num in xrange(len(termDefElements)):
			if num == 0:
				f.write("[Definition]\n")
				f.write(termDefElements[0].text)
			elif num == 1:	
				f.write("\n\n[Break Down]\n")
				f.write(termDefElements[1].text)


		# extract related links
		relatedLinks = soup.find("div", class_="box below-box col-2 no-image gray clear").find_all("a")
		for relatedLink in relatedLinks:
		    fl.write(relatedLink.get("href") + '\n')

		with lock:
			global totalCount
			totalCount += len(termLink)

		f.close()
		fl.close()
	
		
def worker():
    while True:
        letter = q.get()
        getTermLinks(letter)
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
logf = codecs.open(outDir + 'log.txt', encoding='utf-8', mode='a')

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

# write result data
logf.write("--------------------------------------------------------------------\n")
logf.write(str(datetime.now())+'\n')
logf.write("\n# of Pages: %d" % totalCount)
logf.write("\n# of Warnnings: %d\n\n" % warnCount)
logf.close()