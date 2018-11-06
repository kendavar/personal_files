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
    driver=None
    parser = OptionParser()
    parser.add_option("--crawl-textbook", dest="crawl_textbook", action="store_true", help="crawl textbook", default=False)
    parser.add_option("--crawl-textbook-details", dest="crawl_textbook_details", action="store_true", help="crawl textbook details", default=False)

    parser.add_option("--working-dir", dest="workingdir", type="string", help="working directory", default='.')
    parser.add_option("--db-name", dest="db_name", type="string", help="database name", default='opentextbooks')
    parser.add_option("--subject-table-name", dest="subject_table_name", type="string", help="subject table name", default='subject')
    parser.add_option("--textbook-table-name", dest="textbook_table_name", type="string", help="textbook table name", default='opentextbooks')
    parser.add_option("--attachment-table-name", dest="attachment_table_name", type="string", help="attachment table name", default='attachments')
    parser.add_option("--toc-table-name", dest="toc_table_name", type="string", help="toc table name", default='table_of_content')

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
    if options.use_firefox:
        driver = crawlutils.open_driver(use_firefox=options.use_firefox)
    
    try:
        if options.crawl_textbook:
            subjects = db.query("""select * from %s""" %(options.subject_table_name))
            print len(subjects), 'subjects to be crawled yet'
            db.set_autocommit(True)
            count=0
            for (url,subject_title,) in subjects:
                count+=1
                print 'subject title:', subject_title
                print 'url:', url
                print 'subject count :',count
                driver.get(url)
                time.sleep(3)
                ShortDescription=driver.find_elements_by_class_name("ShortDescription")
                for short in ShortDescription:
                   thrid=short.find_element_by_class_name("thrid")
                   img_url=thrid.find_element_by_tag_name("img")
                   h2=short.find_element_by_tag_name("h2")
                   textbook_title=h2.text.strip()
                   textbook_link=h2.find_element_by_tag_name("a").get_attribute("href")
                   m = hashlib.md5()
                   m.update(textbook_title+textbook_link)
                   document_id=m.hexdigest()
                   string=short.find_element_by_tag_name("p").text
                   l=[]
                   if string.find("\n"):
                       authors=string.replace("\n",", ")
                   
                       list=string.split("\n")
                       for a in list:
                           l.append(a.split(",")[0])
                       author=','.join(l)
                   elif string.find(","):
                       authors=string
                       l.append(a.split(",")[0])
                       author=','.join(l)
                   else:
                       authors=string
                       author=string
             
                   print 'textbook_url',textbook_url
                   print 'subject_title',subject_title
                   print 'url',url
                   print 'author',author
                   print 'authors',authors
                   print 'document_id',document_id
                   print 'img_url',img_url
                   data = {
                    'textbook_title':textbook_title,
                    'textbook_url':textbook_url,
                    'subject_title':subject_title,
                    'url':url,
                    'author':author,
                    'authors':authors,
                    'document_id':document_id,
                    'img_url':img_url
                    }
                   db.insert(options.textbook_table_name, data)
                   print "db inserted"
        if options.crawl_textbook_details:
            textbook = db.query("""select document_id,textbook_url from %s where crawled=0""" %(options.textbook_table_name))
            print len(textbook), 'textbook to be crawled yet'
            db.set_autocommit(True)
            count=0
            for (document_id,textbook_url,) in textbook:
                count+=1
                print 'textbook_url:', textbook_url
                print 'document_id:', document_id
                print 'subject count :',count
                driver.get(textbook_url)
                time.sleep(3)

                third=driver.find_element_by_class_name("twothird")
                para= third.find_elements_by_tag_name("p")
                for p in para:
                    para_text=p.text
                    if para_text.startswith("Pub Date:"):
                        pub_date=para_text.replace("Pub Date:","")
                        if pub_date:
                            pub_date=pub_date.strip()
                        else:
                            pub_date=None
                    elif para_text.startswith("ISBN 13:")
                        isbn_13_string=para_text.replace("ISBN 13:","")
                        if isbn_13_string:
                            isbn_13_string=isbn_13_string.strip()
                            isbn_13=isbn_13_string.replace("-","")
                        else:
                            isbn_13_string=None
                            isbn_13=None
                BookTypes=driver.find_element_by_class_name("BookTypes")
                books=BookTypes.find_elements_by_tag_name("a")
                for book in books:
                    attachment_link=book.get_attribute("href")
                    type=book.text.strip()
                    print "attachment_link",attachment_link
                    print "type",type
                    data={
                    "document_id":document_id,
                    "attachment_link":attachment_link,
                    "type":type
                    }
                    db.insert(options.attachment_table_name, data)
                    print "toc table  inserted"
                Badge=driver.find_element_by_class_name("Badge-Condition")
                conditions_text=Badge.text
                condition_link=Badge.find_element_by_tag_name("a").get_attribute("href")
                toc=driver.find_element_by_id("TOC")
                table_of_content=str(toc)
                list_tags=toc.find_elements_by_tag_name("li")
                for list in list_tags:
                    chapter=list.text.strip()
                    if chapter.startswith("Chapter"):
                        chapter_type="Chapter"
                    elif chapter.startswith("Part"):
                        chapter_type="Part"
                    else:
                        chapter_type=None
                    print "title",chapter
                    print "type",chapter_type

                    data={
                    'document_id':document_id,
                    'title':chapter,
                    'type': chapter_type
                    }
                    db.insert(options.toc_table_name, data)
                    print "toc table  inserted"
                AboutBook = driver.find_element_by_id("AboutBook")
                description = AboutBook.text
                links=AboutBook.find_elements_by_tag_name("a")
                for link in links:
                    href = link.get_attribute("href")
                    print "link in books",href
                    data={
                    "document_id":document_id
                    "link":href
                    }
                    db.insert("books", data)
                    print "toc table  inserted"
                AboutAuthors = driver.find_element_by_id("AboutAuthors")
                author_details = AboutAuthors.text
                print 'pub_date',pub_date,
                print 'isbn_13_string',isbn_13_string,
                print 'isbn_13',isbn_13,
                print 'conditions_text',conditions_text,
                print 'condition_link', condition_link,
                print 'table_of_content',table_of_content,
                print 'description',description,
                print 'author_details',author_details
                data = {
                'pub_date':pub_date,
                'isbn_13_string':isbn_13_string,
                'isbn_13':isbn_13,
                'conditions_text': conditions_text,
                'condition_link': condition_link,
                'table_of_content': table_of_content,
                'description' : description,
                'author_details':author_details
                'crawled':1
                }
                db.update(options.textbook_table_name, data, "document_id='%s'" %document_id)

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
