import re
import psycopg2
import requests
import subprocess

import bs4 as BeautifulSoup


conn = psycopg2.connect("dbname=bmo user=bmo password=qsdfghjkl")

traduction_mois = {
 'janvier': '01',
 'février': '02',
 'mars': '03',
 'avril': '04',
 'mai': '05',
 'juin': '06',
 'juillet': '07',
 'août': '08',
 'septembre': '09',
 'octobre': '10',
 'novembre': '11',
 'décembre': '12'
}


def date_to_day(day):
    if day == '1er':
        return '01'
    else:
        return day.rjust(2, '0')


res = requests.get("https://www.paris.fr/bmo")
soup = BeautifulSoup.BeautifulSoup(res.text)
bmo_paragraph = soup.findAll('div', {'class': 'accordion-content-wrapper'})
for bmo_year in bmo_paragraph:
    bmo_list = bmo_year.findAll('a')

    for bmo in bmo_list:
        if bmo.text:
            extract_date = bmo.text.split()[-3:]
            if bool(re.match(r"20\d\d", extract_date[2])):
                date = '{}-{}-{}'.format(extract_date[2],
                                         traduction_mois[extract_date[1]],
                                         date_to_day(extract_date[0]))
                url = bmo['href']
                print(url, date)
                curr = conn.cursor()
                curr.execute("select id from list_pdf where url = %s",
                             (url,))
                if curr.fetchone():
                    continue
                r = requests.get(url, stream=True)
                with open("/tmp/bmo.pdf", "wb") as handle:
                    for chunk in r.iter_content(chunk_size=512):
                        if chunk:  # filter out keep-alive new chunks
                            handle.write(chunk)

                proc = subprocess.run(["pdftotext", "/tmp/bmo.pdf", "-"],
                                      capture_output=True)
                curr.execute("""
                    INSERT INTO list_pdf (url, content, pub_date)
                    VALUES (%s, %s, %s)""", (url, proc.stdout, date))
                conn.commit()
