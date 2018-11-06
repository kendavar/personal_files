#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
import time
import os
import traceback
import codecs
import re
from datetime import datetime
import shutil
import argparse
from PIL import Image
import urllib, cStringIO
import csv
import crawlutils
from optparse import OptionParser
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from selenium import webdriver
import glob

def main():
    urls=[]
    doc_id=[]
    doc_type=[]
    filenames=[]
    doc_not=[]
    #for line in open("url.txt","r") :
    #    urls.append(line.rstrip('\n'))
    folder="./thumbnails/"
    for i,f in enumerate(glob.glob1(folder, "*.png")):
        
        #doc_not.append(f.replace("*.png",""))
    print len(doc_not)
    """with open('ucertify.csv','rb') as csvfile:
        reader=csv.reader(csvfile,delimiter='\t',quotechar='|')
        for row in reader:
            doc_id.append(row[0])
            urls.append(row[1])
            #doc_type.append(row[2])"""
    driver =webdriver.Chrome()
    driver.set_window_size(800,1000)
    
    print len(urls)
    try:
        for number,url in enumerate(urls):
            driver.get(url)
            time.sleep(25)
            filename="/home/vulcantech/kendavar/Ace/screenshot/"+doc_id[number]+".png"
            print doc_id[number]
            #print doc_type[number]
            print filename
            filenames.append(filename)
            driver.save_screenshot(filename)
            crawlutils.resize_png_image(filename)
            time.sleep(2)
            shutil.copyfile(filename, "/home/vulcantech/kendavar/Ace/vi_screenshot_png/"+doc_id[number]+"_png")
            print number
            """
            if doc_type[number] in "webview":
                if "purdueowl" not in url: 
                   driver.get(url)
                   time.sleep(5)
                   filename="/home/vulcantech/kendavar/Ace/screenshot/"+doc_id[number]+".png"
                   print doc_id[number]
                   print doc_type[number]
                   print filename
                   filenames.append(filename)
                   driver.save_screenshot(filename)
                   crawlutils.resize_png_image(filename)
                   time.sleep(2)
                   shutil.copyfile(filename, "/home/vulcantech/kendavar/Ace/vi_screenshot_png/"+doc_id[number]+"_png")
                   print number 
            elif doc_type[number] in "audio":
                url="http://staging.ace.app.writer.pearsonhighered.com/get/thumbnail/b0a4649daeecd82338c45b54a5f20200"
                filename="/home/vulcantech/kendavar/Ace/screenshot/"+doc_id[number]+".png"
                print filename
                filenames.append(filename)
                file = cStringIO.StringIO(urllib.urlopen(url).read())
                img = Image.open(file)
                img.save(filename)
                shutil.copyfile(filename, "/home/vulcantech/kendavar/Ace/vi_screenshot_png/"+doc_id[number]+"_png")
                print number"""
            
        print len(filenames) 
        driver.close()
    except Exception as e:
            print " error",e
            print len(filenames)
            driver.close()

if __name__ == '__main__':
    main()
    

