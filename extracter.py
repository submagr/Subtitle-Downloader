from bs4 import BeautifulSoup
import requests

#Todo : make this load from url dynamic
page = open('release?q=Interstellar.2014.1080p.BluRay.H264.AAC-RARBG')
soup = BeautifulSoup(page)
myTable = soup.table
rows = myTable.tbody.findAll('tr')
# Take Language as input or global parameter set by user
LANGUAGE = 'english'
possible_urls = []  
base_url = 'https://subscene.com'

for row in rows : 
    lan = row.find('span', {'class':'l r neutral-icon'})
    if lan == None : 
        print 'lan None : ', row
        continue
    if lan.lower() == LANGUAGE :
        movie = row.findAll('span')[1].string.rstrip().lstrip()
        sub_url = row.a['href'] 
        possible_urls.append((movie, sub_url))
        #TODO : Find best possible matching string



