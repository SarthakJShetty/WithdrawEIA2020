#!/usr/bin/env python3
import time
from selenium import webdriver
from bs4 import BeautifulSoup as bs

url = 'http://forestsclearance.nic.in/Wildnew_Online_Status_New.aspx'

browser = webdriver.Chrome()
browser.get(url)
browser.find_element_by_id('ctl00_ContentPlaceHolder1_Button1').click()
time.sleep(5)

for counter in range(1, 138):
	proposalElements = []
	'''What needs to be implented here?
	1. Go through the page, scrape all the <span> elements.
	2. Click on the next counter element to go to the next page.
	3. Repeat'''
	csvFile = open('proposal.csv', 'a')
	htmlCode = browser.page_source
	pageSoup = bs(htmlCode, 'html.parser')
	tdElements = pageSoup.findAll('td', {'valign':'top'})
	for tdElement in tdElements:
		if tdElement.find('span'):
			tdElementCleaned = tdElement.find('span').text
			proposalElements.append(str(tdElementCleaned))
	for proposalElement in proposalElements:
		if('FP/' in proposalElement):
			csvFile.write('\n')
		csvFile.write(proposalElement)
		csvFile.write('\t')
	csvFile.close()
	browser.find_element_by_link_text(str(counter+1)).click()
	time.sleep(5)