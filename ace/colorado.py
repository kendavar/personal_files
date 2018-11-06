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

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from optparse import OptionParser

def Main():
    parser = OptionParser()
    parser.add_option("--crawl-textbooks", dest="crawl_textbooks", action="store_true", help="crawl textbooks list", default=False)
    parser.add_option("--working-dir", dest="workingdir", type="string", help="working directory", default='.')
    parser.add_option("--db-name", dest="db_name", type="string", help="database name", default='colorado_1012')
    parser.add_option("--subject2-table-name", dest="subject2_table_name", type="string", help="subject2 table name", default='colorado_subject2')
    parser.add_option("--textbook-table-name", dest="textbook_table_name", type="string", help="textbook table name", default='colorado_textbook')
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
    
    db = mysql.DB(db=options.db_name, port=options.db_port)
    driver = crawlutils.open_driver(use_firefox=options.use_firefox)
    
    try:
        if options.crawl_textbooks:
    
            subject2 = db.query("""select * from %s""" %(options.subject2_table_name))
    
            print len(subject2), 'Textbook to be crawled yet'
            db.set_autocommit(True)
    
            for (subject1_title, subject2_title, subject_url) in subject2:
                print 'subject1_title:', subject1_title
                print 'subject2_title:', subject2_title
                print 'subject_url:', subject_url
                driver.get(subject_url)
                time.sleep(3)
                simulation_link=driver.find_elements_by_class_name("simulation-link")

                for link in simulation_link:
                    file_format=None
                    textbook_url=link.get_attribute("href")
                    textbook_image_url=link.find_element_by_tag_name("img").get_attribute("src")
                    textbook_title=link.find_element_by_tag_name("strong").text
                    span=link.find_element_by_tag_name('span')
                    badge=span[1].get_attribute("class")
                    if "html" in badge:
                        file_format="html5"
                    if "java" in badge:
                        file_format="java applet"
                    if "flash" in badge:
                        file_format="shockwave flash"
                    print "textbook_title :",textbook_title
                    print "textbook_url :",textbook_url
                    print "textbook_image_url :",textbook_image_url
                    print "file_format :",file_format
                    raise Exception("done")

        
                    data = {
                    'subject1_title':subject1_title,
                    'subject2_title':subject2_title,
                    'textbook_title':textbook_title,
                    'textbook_url':textbook_url,
                    'textbook_image_url':textbook_image_url,
                    'format':file_format}
                    db.insert(options.textbook_table_name, data)
                      
       

                
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
