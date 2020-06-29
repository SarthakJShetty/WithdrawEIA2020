#!/usr/bin/env python3
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup as bs

url = 'http://forestsclearance.nic.in/Wildnew_Online_Status_New.aspx'

timeToSleep = 5
pageToStartScrapping = 1

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
browser = webdriver.Chrome(chrome_options=chrome_options)
browser.get(url)
browser.find_element_by_id('ctl00_ContentPlaceHolder1_Button1').click()
time.sleep(timeToSleep)

if pageToStartScrapping != 1:
	try:
		browser.find_element_by_link_text(str(pageToStartScrapping)).click()
		time.sleep(timeToSleep)
	except NoSuchElementException:
		browser.find_element_by_link_text("...").click()
		time.sleep(timeToSleep)
		browser.find_element_by_link_text(str(pageToStartScrapping)).click()
		time.sleep(timeToSleep)

for counter in range(pageToStartScrapping, 138):
	print('Page Number: '+ str(counter))
	proposalElements = []
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
			print('Currently Scrapping Proposal: ' + proposalElement)
			csvFile.write('\n')
		csvFile.write(proposalElement)
		csvFile.write('\t')
	try:
		browser.find_element_by_link_text(str(counter+1)).click()
		time.sleep(timeToSleep)
	except NoSuchElementException:
		browser.find_element_by_link_text("...").click()
		time.sleep(timeToSleep)