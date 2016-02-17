# -*- coding: utf-8 -*-
import urllib2
from bs4 import BeautifulSoup

for numb in ('a', 'a-a3'):

    # fetch htmls from urls
    url = ('http://www.investopedia.com/terms/a/' + numb + '.asp')
    print "\n\n----------------------------------------------------------------"
    print "[term: %s] from (%s)" % (numb, url)
    print "----------------------------------------------------------------"

    # parse htmls to Beautiful object
    html = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html, "lxml")

    # extract definition and break down of term
    contentOfTerm = soup.find("div", class_="content-box content-box-term").p

    print "[Definition]"
    print contentOfTerm.text

    print "\n[Break Down]"
    print "%s\n" % (contentOfTerm.find_next_siblings('p')[0].text)

    # extract links of term
    print "[Links]"
    linkList = soup.find("div", class_="box below-box col-2 no-image gray clear").find_all("a")
    for link in linkList:
        print(link.get("href"))

