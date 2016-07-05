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

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

def extracter(self, videoName):
    # Get Movie Name
    videoName = os.path.splitext(videoName)[0]

    base_url = 'https://subscene.com/'
    response = requests.get(base_url+'subtitles/release?q='+videoName)
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

    self.guiPrint('List of available options : ')
    self.guiPrint(str([url for url in possible_urls]))
    url = process.extractOne(videoName, [url for url in possible_urls])[0]
    subtitle_url = possible_urls[url]
    response = requests.get(base_url + subtitle_url)
    soup = BeautifulSoup(response.content)
    mydiv = soup.find('div', {'class':'download'})
    download_url = base_url + mydiv.a['href']
    response = requests.get(download_url)
    # Extract Zip File 
    subZipFile = StringIO(response.content)
    ZipFile(subZipFile).extractall()
    self.guiPrint('Subtitle file : ' + url + 'downloaded and extracted')
    #TODO : Download all in a directory

class MyWindow(Gtk.Window):
    def __init__(self, videoName):
        self.videoName = videoName
        Gtk.Window.__init__(self, title="subtitle-dl")
        self.button = Gtk.Button(label="Download Subtitle for " + videoName)
        self.button.connect("clicked", self.on_button_clicked)
        self.add(self.button)

    def guiPrint(self, s):
        self.button.set_label(self.button.get_label() + '\n' + s)

    def on_button_clicked(self, widget):
        extracter(self,self.videoName )

win = MyWindow(sys.argv[1])
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
