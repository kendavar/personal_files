#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
import time
import os
import traceback
import codecs
import re
from datetime import datetime
from bs4 import BeautifulSoup as bs
import shutil
import argparse
from PIL import Image
import urllib2
import urllib, cStringIO
import csv
import subprocess as sp

import crawlutils
from optparse import OptionParser

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from selenium import webdriver

def main():
    urls=[]
    filenames=[]
    doc_id=[]
    for line in open("pearson_url.txt","r") :
        urls.append(line.rstrip('\n'))
    #for line in open("vi_doc.txt","r") :
    #    doc_id.append(line.rstrip('\n'))
    #driver =webdriver.Chrome()
    #driver.set_window_size(1280, 1024)
    print len(urls)
    try:
        for number,url in enumerate(urls):
            print url
            res=urllib2.urlopen(url)
            data = res.read()
            time.sleep(2)
            url = re.findall(r'<script src="(.*)"></script>',data)
            res=urllib2.urlopen(url[0])
            time.sleep(2)
            soup = res.read()
            jsonValue = '{%s}' % (soup.split('{', 1)[1].rsplit('}', 1)[0],)
            #print jsonValue
            tmp = jsonValue[jsonValue.find("'html5', config: {'file':"):]
            print tmp
            tmp = tmp.replace("'html5', config: {'file':",'')
            tmp = tmp[:tmp.find("', 'provider': 'video'}")]
            tmp=tmp.replace("'","").strip().replace("\\","")
            print tmp
            filename="/home/vulcantech/kendavar/Ace/vi_screenshot/%s.png"%str(number)
            os.system("""ffmpeg -i %s -ss 00:00:00.435 -vframes 1 /home/vulcantech/kendavar/Ace/vi_screenshot/%s.png"""%(tmp,number))
            #sys.exit()
            #im = im.crop((left, top, right, bottom))
            #im.save(filename)
            print filename
            filenames.append(filename)
            #driver.save_screenshot(filename)
            crawlutils.resize_png_image(filename)
            time.sleep(2)
            print number
            shutil.copyfile(filename, "/home/vulcantech/kendavar/Ace/vi_screenshot_png/%s_png"%str(number))
            #sys.exit()
        driver.quit()           
    except Exception as e:
            print " error",e
            #driver.close()

if __name__ == '__main__':
    main()
