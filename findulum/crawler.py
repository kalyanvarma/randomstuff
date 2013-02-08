from bs4 import BeautifulSoup
import urllib2
import re
from datetime import datetime
import sys

urlroot="http://www.moneycontrol.com"

#Default values for testing
symbol="IT"
year="2012"

if(len(sys.argv)>2):
	symbol=sys.argv[1]
	year=sys.argv[2]

urlextension=urlroot+"/stocks/company_info/stock_news.php?sc_id=" +symbol+ "&durationType=Y&Year=" +year+ "&pageno="
counter=1
pageno=1

while True:

	url=urlextension+str(pageno)
	print "Opening URL [" +url+ "]"
	page = urllib2.urlopen(url)
	soup = BeautifulSoup(page.read())
	divs = soup.find_all('div',class_="MT15 PT10 PB10")
	if not divs:
		print "Does not have news! Finishing."
		break
	for div in divs:
		insidedivs=div.find_all('div', class_="FL")
		for insidediv in insidedivs:
			link=(insidediv.find('a', class_="g_14bl"))
			if(link is None):
				continue
			link=urlroot+link['href']
			title=insidediv.find('strong')
			details=insidediv.find_all('p', class_="PT3")
			times=re.findall(r"\d{1,2}\.\d{1,2}\s[a-zA-Z]{2}\s\|\s\d{2}\s[a-zA-Z]{1,15}\s\d{2,4}", details[0].contents[0])
			if(times):
				timestr=times[0]
			else:
				timestr=""
			date=datetime.strptime(timestr, "%I.%M %p | %d %b %Y")
			summary=details[1].contents[0]
			
			print str(counter)+ ". " +title.string
			print "Time [" +date.strftime('%d-%b-%Y %I:%M %p')+ "]"
			print "Link [" +link+ "]"
			print "Summary [" +summary+ "]\n\n"
			counter+=1

	pageno+=1


#	newspage=urllib2.urlopen(urlroot+link.get('href'))
#	newssoup=BeautifulSoup(newspage.read())
#	titles = newssoup.findAll('h1', class_="gD_40")
#	for title in titles:
#		print "Title is: [" +title.string+ "]"


