#!/user/bin/env python
#_*_ coding:UTF-8 _*_

import requests
import re
import sys
import sqlite3
import logging
import urllib
import glob
import logging
import traceback
import os
import logging
#import MySQLdb
import socket
import time
#import mysql
import crawlutils

from optparse import OptionParser
#from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from bs4 import BeautifulSoup as bs
reload(sys)
sys.setdefaultencoding("utf-8")

def Main():
    parser = OptionParser()
    parser.add_option("--crawl-toc-advanced", dest="crawl_toc", action="store_true", help="crawl chapter content of html", default=False)
  
    parser.add_option("--working-dir", dest="workingdir", type="string", help="working directory", default='.')
    parser.add_option("--filename-name", dest="filename", type="string", help="file where html is stored", default='.')
    parser.add_option("--db-name", dest="db_name", type="string", help="db name", default='textbook_0915')
    parser.add_option("--db-port", dest="db_port", type="int", help="db port", default=3306)
    parser.add_option("--printed_isbn_13", dest="printed_isbn_13", type="string", help="printed isbn 13", default="9780470057650")
    parser.add_option("--textbook_table_name", dest="textbook_table_name", type="string", help="textbook table name", default='wiley_textbook')
    parser.add_option("--skip", dest="skip", type=int, help="integer value", default=0)
    parser.add_option("--use-firefox", dest="use_firefox", action="store_true", help="use-firefox", default=False)
    (options, args) = parser.parse_args()
    
    workingdir = options.workingdir.rstrip('/')
    
    if not os.path.exists(workingdir):
        parser.error("workingdir not exists")
    #db = mysql.DB(db=options.db_name, port=options.db_port)
    driver = crawlutils.open_driver()#use_firefox=options.use_firefox)
    logging.basicConfig(filename='wiley_toc.log',filemode='w',level=logging.DEBUG)
    try:
       if options.crawl_toc:
           advanced_url="http://onlinelibrary.wiley.com/advanced/search?edit=true"
           driver.get(advanced_url)
           time.sleep(3)
           searchText=driver.find_elements_by_class_name('searchText')
           if searchText:
              searchText[0].send_keys(options.printed_isbn_13)
              
           else:
              raise Exception("searchText not found")
           driver.find_element_by_class_name('submit').click()
           time.sleep(3)
           page_wrap=driver.find_elements_by_class_name('page-wrap')
           if not page_wrap:
               raise Exception("page-wrap1 not found")
           content=page_wrap[0].find_elements_by_id('content')
           if not content:
               raise Exception("content1 not found")
           searchResults=content[0].find_elements_by_id('searchResults')
           if not searchResults:
               raise Exception("searchResults1 not found")
           searchResultsList=searchResults[0].find_elements_by_id('searchResultsList')
           if not searchResultsList:
               raise Exception("searchResultsList1 not found")
           articles=searchResultsList[0].find_elements_by_class_name('articles')
           if not articles:
               raise Exception("articles1 not found")
           access=articles[0].find_elements_by_class_name('access')
           if not access:
              raise Exception("access not found")
           doi=access[0].find_elements_by_name('doi')
           if not doi:
              raise Exception("doi not found")
           online_isbn_13=doi[0].get_attribute('value')
           if not len(online_isbn_13):
              raise Exception("value not found")
           online_isbn_13=online_isbn_13.replace('.index',"").strip()
           print online_isbn_13
           online_url="http://onlinelibrary.wiley.com/book/"+online_isbn_13
           driver.get(online_url)
           time.sleep(5)
           page_wrap=driver.find_elements_by_class_name('page-wrap')
           if not page_wrap:
               raise Exception("page-wrap2 not found")
           content=page_wrap[0].find_elements_by_id('content')
           if not content:
               raise Exception("content2 not found")
           books=content[0].find_elements_by_class_name('books')
           if not books:
               raise Exception("books not found")
           chapters=books[0].find_elements_by_class_name('citation')
           
           print dir(chapters[0])
           """if not articles:
               raise Exception("articles2 not found")
           chapters=[]
           for article in articles:
              if article.find_elements_by_class_name('chapter'):
                 chapters.append(article.find_element_by_class_name('chapter'))"""
           if not chapters:
              raise Exception("chapter not found")
           for chapter in chapters:
               productMenu=chapter.find_element_by_class_name('productMenu')
               chap= chapter.text.replace(productMenu.text,"")
               print chap.replace('\n',' ').strip()
    except:          
        traceback.print_exc()
        if driver:
            driver.save_screenshot(workingdir + '/error.png')
            print workingdir + '/error.png'
    
    finally:
        if driver:
            driver.quit()
              


if __name__ == "__main__":
    Main()
            
             
           
           
          
   
