#import psycopg2
import re
import psycopg2
import requests

import bs4 as BeautifulSoup

#div class="accordion-content-wrapper"
traduction_mois = {'janvier':'01', 'février':'02', 'mars':'03', 'avril':'04', 'mai':'05', 'juin':'06', 'juillet':'07', 'août':'08', 'septembre':'09', 'octobre':'10', 'novembre':'11', 'décembre':'12'}

res = requests.get("https://www.paris.fr/bmo")
soup = BeautifulSoup.BeautifulSoup(res.text)
bmo_paragraph = soup.findAll('div', {'class': 'accordion-content-wrapper'})
for bmo_year in bmo_paragraph:
	bmo_list = bmo_year.findAll('a')

	for bmo in bmo_list:
		if bmo.text:
			extract_date = bmo.text.split()[-3:]
			if  bool(re.match("20\d\d", extract_date[2])):
				date = '{}-{}-{}'.format(extract_date[2], traduction_mois[extract_date[1]], '01' if extract_date[0] == '1er' else extract_date[0].rjust(2, '0'))
				print(bmo['href'], date)

def old_version():
	conn = psycopg2.connect("dbname=bmo user=bmo password=qsdfghjkl")
	curr = conn.cursor()


	f=open("tmp.txt", "r")
	contents =f.read()
	contents = contents.split()
	files = {}
	for url in contents:
		#search = re.search('(.*\/)([^\.]+)(\.pdf$|$)', url)
		search = re.search('(.*\/)(.*)($)', url)
		text_name = '{}.txt'.format(search.group(2))
		file = open(text_name, "r")
		content = file.read()
		curr.execute("INSERT INTO list_pdf (url, content) VALUES (%s, %s)", (url, content))
	conn.commit()