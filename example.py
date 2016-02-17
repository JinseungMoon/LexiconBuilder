# -*- coding: utf-8 -*-
import urllib2,sys
from bs4 import BeautifulSoup

for numb in ('a', 'a-a3'):
    address = ('http://www.investopedia.com/terms/a/' + numb + '.asp')
    html = urllib2.urlopen(address).read()
    soup = BeautifulSoup(html)
    
    span = soup.find("div", {"class":"content-box content-box-term"})  # span.string gives you the first bit
    a = [y for y in span.findAllNext("h2")]  
    paras = [x for x in span.findAllNext("p")]
    span1 = soup.find("div", {"class":"box below-box col-2 no-image gray clear"})
    b = [c for c in span1.findAllNext("h3",{"class":"item-title"})]  
    
     
    
    first = "\n\n".join(["".join(y.findAll(text=True)) for y in a[:-1]])
    middle = "\n\n".join(["".join(x.findAll(text=True)) for x in paras[:-1]])
    last = paras[-1].contents[0] 
    final = "\n\n".join(["".join(c.findAll(text=True)) for c in b[:-1]])
    print "%s\n\n%s\n\n%s\n\n%s\n\n" % ( first, middle, last, final)
    
        