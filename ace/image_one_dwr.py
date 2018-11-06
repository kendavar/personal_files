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

def main():
    urls=["http://mediaplayer.pearsoncmg.com/assets/_embed.true/_S4d9GbwzNVKJsky71elZaFdEEyLCW69"]
    filenames=[]
    doc_id=["6fdc7009d956eb2b84fab4af2af6d234"]
    """for line in open("vi_dr12.txt","r") :
        urls.append(line.rstrip('\n'))
    for line in open("vi_doc.txt","r") :
        doc_id.append(line.rstrip('\n'))"""
    driver =webdriver.Chrome()
    driver.set_window_size(1280, 1024)
    print len(urls)
    try:
        for number,url in enumerate(urls):
            print url
            driver.get(url)
            time.sleep(5)
            filename="/home/vulcantech/kendavar/Ace/"+doc_id[number]+".png"   
            print doc_id[number]
            print filename
            element = driver.find_element_by_id('video')
            print element
            location = element.location
            print location
            size = element.size
            print size
            driver.save_screenshot(filename)
            im = Image.open(filename)
            left = location['x']
            print left
            top = location['y']
            print top
            right = location['x'] + size['width']
            print right
            bottom = location['y'] + size['height']
            print bottom
            left=int(round(left))
            right=int(round(right))
            print left,right
            im = im.crop((left, top, right, bottom))
            im.save(filename)
            filenames.append(filename)
            #driver.save_screenshot(filename)
            crawlutils.resize_png_image(filename)
            time.sleep(2)
            print number
            shutil.copyfile(filename, "/home/vulcantech/kendavar/Ace/"+doc_id[number]+"_png")
            #sys.exit()
        driver.quit()           
    except Exception as e:
            print " error",e
            driver.close()

if __name__ == '__main__':
    main()
