import requests, json
from bs4 import BeautifulSoup
from time import sleep


#get urls of all terms
term_urls = []
for term_list_url in [("http://www.investopedia.com/terms/" + letter) for letter in 'abcdefghijklmnopqrstuvwxyz']:
	print "Crawling term urls on", term_list_url
	page = requests.get(term_list_url).text.encode('utf-8').decode('ascii', 'ignore')
	term_list = BeautifulSoup(page , "lxml").find('div', "box col-2 big-item-title clear").ol
	for li in term_list.find_all('li'):
		term_urls.append({'term': li.h3.a.contents[0].strip(),'url': "http://www.investopedia.com" + li.h3.a['href']})
	sleep(1)

with open('term_urls.json', 'w+b') as urls_json:
	json.dump(term_urls, urls_json)
