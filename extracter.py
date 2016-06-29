from bs4 import BeautifulSoup
import requests
from StringIO import StringIO
from zipfile import ZipFile
import requests 
import sys

movie = sys.argv[1]

base_url = 'https://subscene.com/'
response = requests.get(base_url+'subtitles/release?q='+movie)
soup = BeautifulSoup(response.content)
myTable = soup.table
rows = myTable.tbody.findAll('tr')
# Take Language as input or global parameter set by user
LANGUAGE = 'english'
possible_urls = []  

for row in rows : 
    lan = row.find('span', {'class':'l r neutral-icon'})
    if lan == None : 
        print 'lan None : ', row
        continue
    if lan.stripped_strings.next().lower() == LANGUAGE :
        movie = row.findAll('span')[1].string.rstrip().lstrip()
        sub_url = row.a['href'] 
        possible_urls.append((movie, sub_url))

#TODO : Find best possible matching string
subtitle_url = possible_urls[0][1]
response = requests.get(base_url + subtitle_url)
soup = BeautifulSoup(response.content)
mydiv = soup.find('div', {'class':'download'})
download_url = base_url + mydiv.a['href']
response = requests.get(download_url)
subZipFile = StringIO(response.content)
ZipFile(subZipFile).extractall()
