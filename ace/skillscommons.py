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
    parser.add_option("--crawl", dest="crawl", action="store_true", help="crawl url", default=False)
    parser.add_option("--crawl-landing", dest="crawl_landing", action="store_true", help="crawl url", default=False)
    parser.add_option("--working-dir", dest="workingdir", type="string", help="working directory", default='.')
    parser.add_option("--db-name", dest="db_name", type="string", help="database name", default='skillscommons')
    parser.add_option("--table-name", dest="table_name", type="string", help="table name", default='skill')
   
    parser.add_option("--main-table-name", dest="main_table_name", type="string", help="main table name", default='skillscommons')
    parser.add_option("--attachment-table-name", dest="attachment_table_name", type="string", help="attachment table name", default='attachment')
    parser.add_option("--meta-table-name", dest="meta_table_name", type="string", help="meta table name", default='meta_data')
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
    db.set_autocommit(True)
    driver = crawlutils.open_driver(use_firefox=options.use_firefox)
    links=["https://www.skillscommons.org/discover?rpp=2000&page=1&group_by=none&etal=0",
    "https://www.skillscommons.org/discover?rpp=2000&page=2&group_by=none&etal=0",
    "https://www.skillscommons.org/discover?rpp=2000&page=3&group_by=none&etal=0"]
    try:
        if options.crawl:
            
            count = 0
            for link in links:
                print "Link :",link
            
                driver.get(link)
                time.sleep(5)
                medium_results=driver.find_element_by_class_name("medium-results")
                li=medium_results.find_elements_by_tag_name("li")
                for tag in li:
                    count+=1
                    print "Count :",count
                    link_tag=tag.find_element_by_tag_name("a")
                    title=link_tag.text.strip()
                    url=link_tag.get_attribute("href")
                    types=tag.find_elements_by_class_name("type")
                    if len(types)==2:
                        type=types[0].text.strip()
                        institution=types[1].text.strip()
                    else:
                        type=None
                        institution=types[0].text.strip()
                    description=tag.find_element_by_class_name("abstract").text.strip()
                    print "title :", title
                    print "url :",url
                    print "type :",type
                    print "institution :",institution
                    print "description :",description
            
                    data = {
                    'title':title,
                    'institution':institution,
                    'url':url,
                    'type':type,
                    'description':description,
                    }
                    db.insert(options.table_name, data)                      
               

        if options.crawl_landing:
            count=0
            skill=db.query("select distinct url from skill where crawled=0")
            print "Number of urls to crawl ",len(skill)
            for (src_url,) in skill:
                print "source url :",src_url
                print "count %s"%count
                count+=1
                driver.get(src_url)
                author=None
                col=driver.find_element_by_class_name("col-sm-8")
                title=col.find_element_by_tag_name("h1").text.strip()
                m = hashlib.md5()
                m.update(title+src_url)
                document_id=m.hexdigest()
                toc_html="/mnt/data/kendavar/skillscommons/%s.html"%document_id
                file(toc_html,"w","utf8").write(driver.page_source)
                authors=col.find_element_by_class_name("authors")
                if not authors.find_elements_by_tag_name("div"):
                    author=authors.text.strip()
                description=col.find_element_by_class_name("abstract").text
                files=col.find_element_by_class_name("files")
                file_information=files.find_elements_by_class_name("file-information")
                attachment=[]
                for attach in file_information:
                    attachment.append((attach.text.strip(),attach.find_element_by_tag_name("a").get_attribute("href")))
                dls=col.find_elements_by_tag_name("dl")
                meta={}
                string=''
                for dl in dls:
                    for div in dl.find_elements_by_tag_name("div"):
                        string=''
                        dd=div.find_element_by_tag_name("dd")
                        if dd.find_elements_by_tag_name("li"):
                            for li in dd.find_elements_by_tag_name("li"):
                                string=string+li.text.strip()+","
                        elif dd.find_elements_by_tag_name("a"):
                            string=[dd.text.strip()]
                            anchors=[]
                            for anchor in dd.find_elements_by_tag_name("a"):
                                if anchor.get_attribute("href") not in anchors:
                                    anchors.append(anchor.get_attribute("href"))
                                    string.append(anchor.get_attribute("href"))
                        else:
                            string=dd.text.strip()
                        meta[div.find_element_by_tag_name("dt").text.replace(":","").strip()]=string
                print "title :",title
                print "author :",author
                print "description :",description
                print "toc_path",toc_html
                data={
                "document_id":document_id,
                "title":title,
                "author":author,
                "description":description,
                "toc_path":toc_html
                }
                db.insert(options.main_table_name, data) 
                for (attachment_title,attachment_url) in attachment:
                      print "document_id":document_id,
                      print "attachment_title":attachment_title,
                      print "attachment_url":attachment_url
                      data={
                      "document_id":document_id,
                      "attachment_title":attachment_title,
                      "attachment_url":attachment_url
                      }
                      db.insert(options.attachment_table_name, data) 
                for key,value in meta.iteritems():
                      if value[-1]==",":
                          value=value[:-1]
                      print '%s : %s'%(key,value)

                      if type(value) is list:
                          for val in value:
                              meta_title=key
                              if i%2==0 :
                                  meta_value=val
                              else:
                                  meta_url=val
                              print "meta_title":meta_title
                              print "meta_value":meta_value
                              print "meta_url":meta_url
                              data={
                              "document_id":document_id,
                              "meta_title":meta_title,
                              "meta_value":meta_value,
                              "meta_url":meta_url
                              }
                              db.insert(options.meta_table_name, data)
                      else:
                          meta_title=key
                          meta_url=None
                          meta_value=value
                          print "meta_title":meta_title
                          print "meta_value":meta_value
                          print "meta_url":meta_url
                          data={
                          "document_id":document_id,
                          "meta_title":meta_title,
                          "meta_value":meta_value,
                          "meta_url":meta_url
                          }
                          db.insert(options.meta_table_name, data)
                data={
                "crawled":1
                }
                db.update(options.table_name,data,"url='%s'"%src_url)
                print "updated the table"

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
