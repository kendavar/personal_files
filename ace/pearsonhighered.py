#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import mysql
from src import crawlutils
import hashlib
import os
import time
import codecs
import MySQLdb
import traceback
import mx.DateTime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from optparse import OptionParser

def Main():
    parser = OptionParser()
    parser.add_option("--textbook-package", dest="textbook_package", action="store_true", help="textbook package details", default=False)
    parser.add_option("--working-dir", dest="workingdir", type="string", help="working directory", default='.')
    parser.add_option("--db-name", dest="db_name", type="string", help="db name", default='pearsonhighered')
    parser.add_option("--db-port", dest="db_port", type="int", help="db port", default=3306)
    parser.add_option("--textbook-package-table-name", dest="textbook_package_table_name", type="string", help="textbook package table name", default='textbook_package')
    parser.add_option("--pearsonhighered-textbooks-table-name", dest="pearsonhighered_textbooks_table_name", type="string", help="subject2 table name", default='pearsonhighered_textbooks')
   
    parser.add_option("--skip", dest="skip", type=int, help="integer value", default=0)
    parser.add_option("--use-firefox", dest="use_firefox", action="store_true", help="use-firefox", default=False)
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
        if options.crawl_subjects1:
            textbooks = db.query("""select textbook_id,textbook_url from pearsonhighered_textbooks where status=0'""" %(options.textbook_package_table_name))
    
            print len(textbooks), 'textbooks yet to be crawled'
            db.set_autocommit(True)
    
            count = 0        
            for (textbook_id,textbook_url) in textbooks:
                count += 1
                print 'count:', count
                print 'textbook_id:',textbook_id
                print 'textbook_url:', textbook_url
                if not textbook_url:
                    continue    
                driver.get(textbook_url)
                time.sleep(3)
                tab_content_group=driver.find_elements_by_class_name("tab-content group")

                if not tab_content_group:
                   raise Exception "tab-content group not found"
                data_feed_float_right=tab_content_group[0].find_elements_by_class_name("data-feed float-right")
                if data_feed_float_right:
                   raise Exception "data-feed float-right no found"
                description=data_feed_float_right[0].find_elements_by_id("description")
                if not description:
                   raise Exception "description not found"
                ul=description[0].find_elements_by_tag_name("ul")
                
                if not ul:
                   raise  Exception "ul tag not found"
                while True:
                    a=ul[0].find_elements_by_tag_name("a")
                    if not a:
                      raise  Exception "a tag not found"
                    textbook_title=a[0].text.strip()
                    p=ul[0].find_elements_by_tag_name("p")
                    if not p:
                      raise  Exception "p tag not found"
                    if len(p)==3:
                      raise  Exception "all p tags are not found"
                    for tag in p:
                       package_details=tag.text
                       if '©' in package_details:
                          copy_right_year=package_details[package_details.find("©")+1:package_details.find("•")]
                          copy_right_year=copy_right_year.strip()
                          if not len(copy_right_year)==4:
                             raise  Exception "copy right right is not correct" 
                          if 'pp' in package_details:
                             pages=package_details[package_details.find(",")+1:package_details.find("pp")]
                             pages=pages.strip()
                       print "copy right year",copy_right_year
                       print "Pages",pages
                       if "ISBN" in package_details:
                          if "•" in package_details:
                             isbns=package_details.split("•")
                          for isbn in isbns:
                             if "ISBN-10:" in isbn:
                                isbn_10=isbn.replace("ISBN-10:","").strip()
                             if "ISBN-13:" in isbn:
                                isbn_13=isbn.replace("ISBN-13:","").strip()
                             if not len(isbn_10)==10:
                                raise  Exception "isbn 10 is not correct"
                             if not len(isbn_13)==13:
                                raise  Exception "isbn 13 is not correct"
                       print "isbn_10 :",isbn_10
                       print "isbn_13 :",isbn_13
                       author=package_details.strip()
                       print "author :",author
                    data = {'textbook_title':title,'textbook_isbn_10':textbook_isbn_10,'textbook_isbn_13':textbook_isbn_13,
                            'textbook_author':author, 'textbook_copyright_year':textbook_copyright_year,'pages':pages,  
                            'status':1}
                    db.update(options.textbook_table_name, data, "textbook_url='%s'" %textbook_url)
                    time.sleep(3)
                    next=description[0].find_element_by_xpath("//ul/following-sibling::ul")      
                    if next:
                       print "Next sibling found"
                       ul=next
                    else:
                       print "next sibling not found"
                       break

       
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
    
   
