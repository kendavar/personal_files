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
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import TimeoutException



import crawlutils
from optparse import OptionParser

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from selenium import webdriver
import glob

def main():
    urls=[]
    filenames=[]
    doc_id=[]
    duplicates=[]
    doc_not=[]
    i=0
    with open('mylab.csv','rb') as csvfile:
        reader=csv.reader(csvfile,delimiter=',',quotechar='"')
        for row in reader:
            doc_id.append(row[0])
            #urls.append(row[1])
    folder="/home/vulcantech/kendavar/Ace/vi_screenshot_png/"
    for i,f in enumerate(glob.glob1(folder, "*_png")):
        doc_not.append(f.replace("_png",""))
        
    print len(doc_not)
    print doc_not[1]
    driver =webdriver.Chrome()
    driver.set_window_size(1000, 900)
    loginurl = "https://portal.mypearson.com/login"
    driver.get(loginurl)
    time.sleep(5)
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "username"))).send_keys("ace_learning")
    driver.find_element_by_id('password').send_keys("ACE15Pearson")
    driver.find_element_by_id('mainButton').click()
    time.sleep(10)

    #print len(urls)
    try:
        for number,doc_ids in enumerate(doc_id):
            filename="/home/vulcantech/kendavar/Ace/vi_screenshot/%s.png"%(doc_ids) 
            driver.get("http://www.learningace.com/get/thumbnail/"+doc_ids)
            time.sleep(10)  
            #print doc_id[number]
            #print filename
            #print url
            #if doc_id[number] in doc_not:
            #    continue
            if filename in filenames:
                duplicates.append(doc_id)
                #continue
            if ".pptx" in url:
                print doc_id[number]
                print url
            if ".ppt" in url:
                print "skiped",i
                continue
            continue
            if "triolafc" in url:
                driver.set_window_size(1000, 900)
            elif "mediaplayer" in url:
                driver.set_window_size(1000, 900)
            else:
                driver.set_window_size(800, 900)
            driver.get(url)
            time.sleep(20)    
            if ".html" not in url:
                ##main code for getting the thumbnail
                element = driver.find_element_by_tag_name('object')
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
            else:
            driver.save_screenshot(filename)
            filenames.append(filename)
            
            #driver.save_screenshot(filename)
            crawlutils.resize_png_image(filename)
            time.sleep(2)
            print number
            shutil.copyfile(filename, "/home/vulcantech/kendavar/Ace/vi_screenshot_png/%s_png"%(doc_id[number]))
            #sys.exit()"""
        print "duplicates :",len(duplicates)
        driver.quit()           
    except Exception as e:
            print " error",e
            driver.close()

if __name__ == '__main__':
    main()
