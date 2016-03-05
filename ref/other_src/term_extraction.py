import requests, json
from bs4 import BeautifulSoup
from time import sleep

#load term urls and remove crawled urls
with open('term_url_list.json') as f:
	complete_term_list = json.load(f)

with open('crawled_term_url_list.json') as f:
	crawled_term_list = json.load(f)

crawled_terms = [t['term'] for t in crawled_term_list]
term_list = []
for term in complete_term_list:
	if term['term'] not in crawled_terms:
		term_list.append(term)

#load crawled terms
with open('terms.json') as tjf:
	terms = json.load(tjf)

#crawl
for term_item in term_list:
	term = {}
	term['url'] = term_item['url']
	term['term'] = term_item['term']

	print "Crawling Term", term['term'], "on", term['url']

	url = term['url']
	term_page = BeautifulSoup(requests.get(url).text.encode('utf-8').decode('ascii', 'ignore'), "lxml")

	#definition
	p_tags = term_page.find_all(['h2', 'p'])
	definition = ''
	for tag in p_tags[1:]:
		if tag.name == 'h2':
			break
		definition += ''.join(tag.find_all(text=True))
	term['definition'] = definition.strip()

	#breakingdown
	p_tags.reverse()
	breakingdown = ''
	for tag in p_tags:
		if tag.name == 'h2':
			break
		breakingdown = ''.join(tag.find_all(text=True)) + breakingdown
	term['breakingdown'] = breakingdown.strip()

	#related terms
	related_terms = []
	try:
		related_terms_ol = term_page.find('div', "box below-box col-2 no-image gray clear").ol
		for a in related_terms_ol.find_all('a'):
			related_terms.append({'term': a.contents[0].strip(), 'url': "http://www.investopedia.com" + a['href']})
		term['related_terms'] = related_terms
	except AttributeError:
		pass

	#related articles
	related_articles = []
	try:
		related_articles_ol = term_page.find('div', {'id': "term_ArticlesOfInterest"}).ol
		for li in related_articles_ol.find_all('li'):
			title = li.h3.a.contents[0].strip()
			category = li.find('div', "item-category").contents[0].strip()
			url = ("" if category.find('SPONSORED') >= 0 else "http://www.investopedia.com") + li.h3.a['href']
			related_articles.append({'title': title, 'category': category, 'url': url})
		term['related_articles'] = related_articles
	except AttributeError:
		pass

	#related FAQ
	related_faqs = []
	try:
		related_faqs_ol = term_page.find('div', {'id': "bl_term_ralated_faqs"}).ol
		for li in related_faqs_ol.find_all('li'):
			question = li.h3.a.contents[0].strip()
			url = "http://www.investopedia.com" + li.h3.a['href']
			related_faqs.append({'question': question, 'url': url})
		term['related_faqs'] = related_faqs
	except AttributeError:
		pass

	#update terms.json and crawled_term_list.json after crawling every 20 terms
	terms.append(term)
	crawled_term_list.append(term_item)
	if (len(terms) % 20 == 0):
		with open('terms.json', 'w+b') as tjf:
			json.dump(terms, tjf)
		
		with open('crawled_term_url_list.json', 'w+b') as ctjf:
			json.dump(crawled_term_list, ctjf)

	#crawl politely
	sleep(1)

with open('terms.json', 'w+b') as tjf:
	json.dump(terms, tjf)

with open('crawled_term_url_list.json', 'w+b') as ctjf:
	json.dump(crawled_term_list, ctjf)
