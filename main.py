# -*- coding: utf-8 -*-
import etr
import string
import os
import codecs
from datetime import datetime

# initial properties
baseUrl = "http://www.investopedia.com"
#letterList = '1abcdefghijklmnopqrstuvwxyz'
letterList = 'stuvwxyz'
termLinks = list()

# extract links from each letter("#~Z")
for termIdx in letterList:
    termLinks.append(etr.getTermLinks(termIdx))

# write all data into separate txt file
totalCount = 0
warnCount = 0
outDir = os.getcwd() + "/out/"
logf = codecs.open(outDir + 'log.txt', encoding='utf-8', mode='a')

for i in xrange(len(letterList)):
	termCount = 0
	for termLink in termLinks[i]:

		termUrl = baseUrl + termLink
		#termUrl = "http://www.investopedia.com/terms/p/ppipla.asp"
		
		print "%s\n" % (termUrl) 
	
		# write on a txt file
		filePath = outDir + termUrl[len(baseUrl)+1:].rstrip(".asp") + ".txt"
		linkfilePath = filePath.rstrip(".txt") + "_RT.txt"

		targetDir = os.path.dirname(filePath)
		if not os.path.exists(targetDir):
		    os.makedirs(targetDir)

		f = codecs.open(filePath, encoding='utf-8', mode='w')
		fl = codecs.open(linkfilePath, encoding='utf-8', mode='w')


		 # extract definition and break down of term
		soup = etr.getSoup(termUrl)
		termDefElements = soup.find("div", class_="content-box content-box-term").find_all('p') 

		if len(termDefElements) <= 1:
			logf.write(str('[Invalid Format!]' + termLink + '\n'))
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

		termCount += len(termLinks)
		f.close()
		fl.close()
		
		# print '\'' + filePath + '\'' + ' written'
		# print '\'' + linkfilePath + '\''+ ' written'
	
	print ("total number pages from letter '%s' = %d\n") % (letterList[i], termCount)
	totalCount += termCount


# write result data
logf.write(str(datetime.now())+'\n')
for letter in letterList[i]:
	logf.write("['%s': %d] " % (letter.upper(), termCount)) 
logf.write("\n# of Pages: %d" % totalCount)
logf.write("\n# of Warnnings: %d\n\n" % warnCount)
logf.write("--------------------------------------------------------------------\n")
logf.close()