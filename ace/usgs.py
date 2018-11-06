#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from src import mysql
from src import crawlutils
import hashlib
import os
import urllib
import time
from bs4 import BeautifulSoup as bs
import codecs
import MySQLdb
import traceback
import requests
import mx.DateTime
import shutil

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from optparse import OptionParser

from src import crawltext

def save(tag,subject1,subject2):
    link=tag.a["href"]
    title=tag.a.text
    h = hashlib.md5()
    h.update(link+title)
    document_id= h.hexdigest()
    [e.extract() for e in tag.findAll('a')]
    description=tag.text.strip()
    print "document_id :",document_id
    print "link :",link
    print "title :",title
    print "description :",description
    data = {
    'link': link,
    'title': title,
    'subject1': subject1,
    'subject2': subject2,
    'description': description,
    'document_id': document_id
     }
    db.insert(options.table_name, data)
    print "db inserted"

def Main():
    driver=None
    parser = OptionParser()
    parser.add_option("--crawl", dest="crawl", action="store_true", help="crawl textbook", default=False)
    parser.add_option("--details", dest="details", action="store_true", help="crawl textbook details", default=False)

    parser.add_option("--working-dir", dest="workingdir", type="string", help="working directory", default='.')
    parser.add_option("--db-name", dest="db_name", type="string", help="database name", default='usgs')

    parser.add_option("--table-name", dest="table_name", type="string", help="textbook table name", default='usgs')
    parser.add_option("--skip", dest="skip", type=int, help="integer value", default=0)
    parser.add_option("--use-firefox", dest="use_firefox", action="store_true", help="use-firefox", default=True)
    (options, args) = parser.parse_args()
    
    workingdir = options.workingdir.rstrip('/')
    
    if not os.path.exists(workingdir):
        parser.error("workingdir not exists")
    
    try:
        display = None
        from pyvirtualdisplay import Display
        display = Display(visible=0, size=(1000,900))
        display.start()
    except:
        print 'No Xvfb!'
    
    db = mysql.DB(db=options.db_name)
    #if options.use_firefox:
    #    driver = crawlutils.open_driver(use_firefox=options.use_firefox)
    
    try:
        if options.crawl:
            res=requests.get("http://education.usgs.gov/undergraduate.html")
            soup=bs(res.text)
            td=soup.findAll("td")
            subject2=None
            for i,tag in enumerate(td):
                if i >= 5 :
                    if tag.find("h2"):   
                        subject1=tag.text.strip()
                    elif len(tag.findAll("hr"))==2:
                        if tag.find("div"):
                            tag.div.extract()
                        subject2=tag.text.strip() 
                        print subject2
                    elif tag.find("a"):
                        if tag.find("li"):
                            if not tag.find("strong"):
                                tag.a.extract()
                                description=tag.text.strip()
                            for list1 in tag.findAll("li"):
                                save(list1,subject1,subject2)
                                
                        else:
                            save(tag,subject1,subject2)
                    

            
           
        if options.details:
            links = db.query("""select document_id,link from %s where crawled=0""" %(options.table_name))
            print len(links), 'links to be crawled yet'
            db.set_autocommit(True)
            count=0
            for (document_id,link,) in links:
                count+=1
                print 'link:', link
                print 'document_id:', document_id
                print 'link count :',count
                documents=(document_id,link)
                txt_location,driver=crawl_documents(documents, '/mnt/data/kendavar/usgs') 
                driver.set_window_size(1000,900)
                filename="/mnt/data/kendavar/usgs/screenshots/%s.png"%document_id
                driver.save_screenshot(filename)
                crawlutils.resize_png_image(filename)
                img_location="/mnt/data/kendavar/usgs/screenshot_png/%s_png"%document_id
                shutil.copyfile(filename,img_location )
                data = {
                'screenshot':img_location,
                'txt_location':txt_location,
                'crawled':1
                }
                db.update(options.table_name, data, "document_id='%s'" %document_id)

    except:
        traceback.print_exc()
        if driver:
            driver.save_screenshot(workingdir + '/error.png')
            print workingdir + '/error.png'
    
    finally:
        if driver:
            driver.quit()
        if display:
            display.stop()




if __name__ == "__main__":
    Main()
