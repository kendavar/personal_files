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
    parser.add_option("--crawl", dest="crawl", action="store_true", help="crawllist", default=False)
    parser.add_option("--working-dir", dest="workingdir", type="string", help="working directory", default='.')
    parser.add_option("--db-name", dest="db_name", type="string", help="database name", default='ted')
    parser.add_option("--topic-table-name", dest="topic_table_name", type="string", help="topic table name", default='ted_topics')
    parser.add_option("--ted-table-name", dest="ted_table_name", type="string", help="ted table name", default='ted')
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
    driver = crawlutils.open_driver(use_firefox=options.use_firefox)
    
    try:
        if options.crawl:
    
            topics = db.query("""select * from %s""" %(options.topic_table_name))
    
            print len(topics), 'Topics to be crawled yet'
            db.set_autocommit(True)
            count=0
            for (topic,topic_url,) in topics:
                count+=1
                print 'topic:', topic
                print 'topic_url:', topic_url
                print 'topic count :',count
                driver.get(topic_url)
                time.sleep(3)
                pagination=driver.find_elements_by_class_name("pagination")
                number=0
                if pagination:
                    atag=pagination[0].find_elements_by_tag_name("a")
                    page_numbers=int(atag[-2].text.encode("utf-8"))
                    print "Page numbers ",page_numbers
                    for page_number in range(page_numbers):
                        number+=1
                        url="https://www.ted.com/talks?page=%s&sort=newest&topics[]=%s"%(str(page_number+1),topic)
                        url=url.replace(" ","+")
                        print "Page url :",url
                        print "page number :",number
                        driver.get(url)
                        time.sleep(3)
                        crawl_data(driver,options,db,topic)
                else:
                    print "Paginator not found"
                    crawl_data(driver,options,db,topic)

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


def crawl_data(driver,options,db,topic):
    index=0
    talk_links=driver.find_elements_by_class_name("talk-link")
    for talk_link in talk_links:
        index+=1
        img_url=talk_link.find_element_by_tag_name("img").get_attribute("src")
        h4=talk_link.find_elements_by_tag_name("h4")
        author=h4[0].text.strip()
        link=h4[1].find_element_by_tag_name("a")
        title=link.text.strip()
        link=link.get_attribute("href")
        meta=talk_link.find_element_by_class_name("meta")
        meta__item=meta.find_element_by_class_name("meta__item")
        posted=meta__item.find_element_by_class_name("meta__val").text.strip()
        meta__row=meta.find_element_by_class_name("meta__row")
        rated=meta__row.find_element_by_class_name("meta__val").text.strip()


        print 'topic :',topic
        print 'title :',title
        print 'link :',link
        print 'author :',author
        print 'posted :',posted
        print 'rated :',rated
        print 'img_url :',img_url
        print 'Number of talks :',index
        data = {
        'topic':topic,
        'title':title,
        'link':link,
        'author':author,
        'posted':posted,
        'rated':rated,
        'img_url':img_url
        }
        db.insert(options.ted_table_name, data)
        print "db inserted"


if __name__ == "__main__":
    Main()
