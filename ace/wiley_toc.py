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

from optparse import OptionParser
#from selenium.common.exceptions import TimeoutException
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium import webdriver
from bs4 import BeautifulSoup as bs
reload(sys)
sys.setdefaultencoding("utf-8")

def Main():
    parser = OptionParser()
    parser.add_option("--crawl-toc", dest="crawl_toc", action="store_true", help="crawl chapter content of html", default=False)
  
    parser.add_option("--working-dir", dest="workingdir", type="string", help="working directory", default='.')
    parser.add_option("--filename-name", dest="filename", type="string", help="file where html is stored", default='.')
    parser.add_option("--db-name", dest="db_name", type="string", help="db name", default='textbook_0915')
    parser.add_option("--db-port", dest="db_port", type="int", help="db port", default=3306)
    parser.add_option("--textbook_toc_table_name", dest="textbook_toc_table_name", type="string", help="textbook toc table name", default="textbook_toc")
    parser.add_option("--textbook_table_name", dest="textbook_table_name", type="string", help="textbook toc table name", default='wiley_textbook')
   
   
    parser.add_option("--skip", dest="skip", type=int, help="integer value", default=0)
    parser.add_option("--use-firefox", dest="use_firefox", action="store_true", help="use-firefox", default=False)
    (options, args) = parser.parse_args()
    
    workingdir = options.workingdir.rstrip('/')
    
    if not os.path.exists(workingdir):
        parser.error("workingdir not exists")
    #db = mysql.DB(db=options.db_name, port=options.db_port)
    logging.basicConfig(filename='wiley_toc.log',filemode='w',level=logging.DEBUG)
    try:
       if options.crawl_toc:
          #textbook=db.query("select id,textbook_url from %s where toc = 1 and id not in (select distinct id from %s)""" %(options.textbook_table_name, options.textbook_toc_table_name))
          textbook=[("13ca5b0f9f78cfcfd1df447a2a727278","")]
          print "Textbook toc to crawl",len(textbook)
          for (textbook_id,textbook_url) in textbook:
              toc_html_file=workingdir+'/'+options.filename+'/'+textbook_id+'.html'
              f=open(toc_html_file,"r")
              f.close
              toc_html=f.read()
              toc_html = toc_html.replace('<i>', '').replace('</i>', '').replace('<b>', '').replace('</b>', '')
              toc_html = toc_html.replace("<br>", " ")
              toc_html = toc_html.replace("""<st1:country-region w:st="on"><st1:place w:st="on">""","").replace("</st1:place></st1:country-region>","")
              soup=bs(toc_html)
              toc = soup.find('body')
              if not toc:
                  print toc_html
                  raise Exception('no body')
              p_tag=soup.findAll('p')
              print p_tag
              if not p_tag:
                 print toc_html,textbook_url
                 #raise Exception('no p tag')
              chapters=[]
              for tag in toc_html.split('\n'):
                  print tag
              for tag in p_tag:
                 if tag.findChildren():
                         continue 
            
              for tag in p_tag:
                  string=tag.text
                  chapters.append(tag.text)
              for chapter in chapters:
                 data={'id':textbook_id,'title':chapter,'textbook_url':textbook_url,'seq_num':seq_num}
                 print data
                 #db.update(options.textbook_table_name, data, "textbook_url='%s'" %textbook_url)
                 time.sleep(2)
                 print "File %s is crawled"%(textbook_id+'.html') 
    except:          
        traceback.print_exc()
              


if __name__ == "__main__":
    Main()
            
             

