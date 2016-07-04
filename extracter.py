#!/usr/bin/env python
from bs4 import BeautifulSoup
import requests
from StringIO import StringIO
from zipfile import ZipFile
import requests 
import sys
import os
from fuzzywuzzy import process
from pprint import pprint

# Get Movie Name
movie = sys.argv[1]
movie = os.path.splitext(movie)[0]

base_url = 'https://subscene.com/'
response = requests.get(base_url+'subtitles/release?q='+movie)
soup = BeautifulSoup(response.content)
myTable = soup.table
rows = myTable.tbody.findAll('tr')

LANGUAGE = 'english'
possible_urls = {}  

for row in rows : 
    lan = row.find('span', {'class':'l r neutral-icon'})
    if lan == None : 
        continue
    if lan.stripped_strings.next().lower() == LANGUAGE :
        name = row.findAll('span')[1].string.rstrip().lstrip()
        sub_url = row.a['href'] 
        possible_urls[name] =  sub_url

print 'List of available options : '
pprint([url for url in possible_urls])
url = process.extractOne(movie, [url for url in possible_urls])[0]
subtitle_url = possible_urls[url]
response = requests.get(base_url + subtitle_url)
soup = BeautifulSoup(response.content)
mydiv = soup.find('div', {'class':'download'})
download_url = base_url + mydiv.a['href']
response = requests.get(download_url)
# Extract Zip File 
subZipFile = StringIO(response.content)
ZipFile(subZipFile).extractall()
print 'Subtitle file : ', url, 'downloaded and extracted'  
#TODO : Download all in a directory

