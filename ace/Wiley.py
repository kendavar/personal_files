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
    parser.add_option("--crawl-subjects1", dest="crawl_subjects1", action="store_true", help="crawl first level subjects", default=False)
    parser.add_option("--crawl-subjects2", dest="crawl_subjects2", action="store_true", help="crawl second level subjects", default=False)
    parser.add_option("--crawl-subjects3", dest="crawl_subjects3", action="store_true", help="crawl third level subjects", default=False)
    parser.add_option("--crawl-subjects4", dest="crawl_subjects4", action="store_true", help="crawl fourth level subjects", default=False)
    parser.add_option("--crawl-textbooks", dest="crawl_textbooks", action="store_true", help="crawl textbooks list", default=False)
    parser.add_option("--crawl-textbook-details", dest="crawl_textbook_details", action="store_true", help="crawl textbooks details", default=False)
    parser.add_option("--working-dir", dest="workingdir", type="string", help="working directory", default='.')
    parser.add_option("--db-name", dest="db_name", type="string", help="db name", default='textbook_0915')
    parser.add_option("--db-port", dest="db_port", type="int", help="db port", default=6606)
    parser.add_option("--subject1-table-name", dest="subject1_table_name", type="string", help="subject1 table name", default='wiley_subject1')
    parser.add_option("--subject2-table-name", dest="subject2_table_name", type="string", help="subject2 table name", default='wiley_subject2')
    parser.add_option("--subject3-table-name", dest="subject3_table_name", type="string", help="subject3 table name", default='wiley_subject3')
    parser.add_option("--subject4-table-name", dest="subject4_table_name", type="string", help="subject4 table name", default='wiley_subject4')
    parser.add_option("--textbook-table-name", dest="textbook_table_name", type="string", help="textbook table name", default='wiley_textbook')
    parser.add_option("--journal-table-name", dest="journal_table_name", type="string", help="journal table name", default='wiley_journal')
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
            url = "http://as.wiley.com/WileyCDA/Section/index.html"
            driver.get(url)
            hoverlist = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "subjects-hoverlist")))
            db.set_autocommit(False)
    
            index = 0
            for a in hoverlist.find_elements_by_xpath("./li/a"): 
                index += 1
                print 'index:', index
                subject1_title = a.text.strip()
                print 'subject1_title:', subject1_title
                subject1_url = a.get_attribute('href')
                print 'subject1_url:', subject1_url
                data = {'subject1_title':subject1_title, 'subject1_url':subject1_url}
                db.insert(options.subject1_table_name, data)
            db.commit()
    
        if options.crawl_subjects2:
    
            subjects1 = db.query("""select subject1_title, subject1_url from %s where subject1_title not in (select distinct subject1_title from %s)
                                               """ %(options.subject1_table_name, options.subject2_table_name))
    
            print len(subjects1), 'subjects1 yet to be crawled'
            db.set_autocommit(True)
    
            for (subject1_title, subject1_url) in subjects1:
                print 'subject1_title:', subject1_title
                print 'subject1_url:', subject1_url
                driver.get(subject1_url)
                
                hoverlist = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "subjects")))
                index = 0
                for a in hoverlist.find_elements_by_xpath("./li/a"): 
                    index += 1
                    print 'index:', index
                    subject2_title = a.text.strip()
                    print 'subject2_title:', subject2_title
                    subject2_url = a.get_attribute('href')
                    print 'subject2_url:', subject2_url
                    data = {'subject1_title':subject1_title, 'subject2_title':subject2_title, 'subject2_url':subject2_url}
                    db.insert(options.subject2_table_name, data)
                db.commit()
                time.sleep(3)
    
     
        if options.crawl_subjects3:
    
            subjects2 = db.query("""select a.subject1_title, a.subject2_title, a.subject2_url from %s a left join %s b on a.subject1_title=b.subject1_title and a.subject2_title=b.subject2_title where b.subject1_title is null
                                               """ %(options.subject2_table_name, options.subject3_table_name))
    
            print len(subjects2), 'subjects2 yet to be crawled'
            db.set_autocommit(False)
    
            for (subject1_title, subject2_title, subject2_url) in subjects2:
                print 'subject1_title:', subject1_title
                print 'subject2_title:', subject2_title
                print 'subject2_url:', subject2_url
                driver.get(subject2_url)
                time.sleep(3)
                try:
                    hoverlist = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "subjectsbox")))
                    hoverlist = hoverlist.find_elements_by_xpath("./ul[@class='subjects']")
                except:
                    print "subjects not found. so crawling textbook listing"
                    data = {'subject1_title':subject1_title, 'subject2_title':subject2_title, 'subject3_title':'', 'subject3_url':subject2_url}
                    db.insert(options.subject3_table_name, data)
                    db.commit()
                    crawl_textbook_listing(driver, db, workingdir, options, subject1_title, subject2_title, '', '')
                    continue
                       
                index = 0
                for a in hoverlist.find_elements_by_xpath("./li/a"): 
                    index += 1
                    print 'index:', index
                    subject3_title = a.text.strip()
                    print 'subject3_title:', subject3_title
                    subject3_url = a.get_attribute('href')
                    print 'subject3_url:', subject3_url
                    data = {'subject1_title':subject1_title, 'subject2_title':subject2_title, 'subject3_title':subject3_title, 'subject3_url':subject3_url}
                    db.insert(options.subject3_table_name, data)
                db.commit()
                time.sleep(3)
    
        if options.crawl_subjects4:
    
            subjects3 = db.query("""select a.subject1_title, a.subject2_title, a.subject3_title, a.subject3_url from %s a left join %s b on a.subject1_title=b.subject1_title and a.subject2_title=b.subject2_title and a.subject3_title=b.subject3_title where b.subject1_title is null
                                               """ %(options.subject3_table_name, options.subject4_table_name))
    
            print len(subjects3), 'subjects3 yet to be crawled'
            db.set_autocommit(False)
    
            for (subject1_title, subject2_title, subject3_title, subject3_url) in subjects3:
                print 'subject1_title:', subject1_title
                print 'subject2_title:', subject2_title
                print 'subject3_title:', subject3_title
                print 'subject3_url:', subject3_url
                driver.get(subject3_url)
                time.sleep(3)
                
                if not subject3_title:
                    print "subject3_title is empty"
                    data = {'subject1_title':subject1_title, 'subject2_title':subject2_title, 'subject3_title':subject3_title, 'subject4_title':'', 'subject4_url':subject3_url}
                    db.insert(options.subject4_table_name, data)
                    db.commit()
                    continue                
                
                try:
                    hoverlist = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "subjectsbox")))
                    hoverlist = hoverlist.find_elements_by_xpath("./ul[@class='subjects']")
                except:
                    data = {'subject1_title':subject1_title, 'subject2_title':subject2_title, 'subject3_title':subject3_title, 'subject4_title':'','subject4_url':subject3_url}
                    db.insert(options.subject4_table_name, data)
                    db.commit()
                    crawl_textbook_listing(driver, db, workingdir, options, subject1_title, subject2_title, subject3_title, '')
                    continue
                       
                index = 0
                for a in hoverlist.find_elements_by_xpath("./li/a"): 
                    index += 1
                    print 'index:', index
                    subject4_title = a.text.strip()
                    print 'subject4_title:', subject4_title
                    subject4_url = a.get_attribute('href')
                    print 'subject4_url:', subject4_url
                    data = {'subject1_title':subject1_title, 'subject2_title':subject2_title, 'subject3_title':subject3_title,'subject4_title':subject4_title, 'subject4_url':subject4_url}
                    db.insert(options.subject4_table_name, data)
                db.commit()
                time.sleep(3)
                
        if options.crawl_textbooks:
    
            subjects4 = db.query("""select a.subject1_title, a.subject2_title, a.subject3_title, a.subject4_title, a.subject4_url from %s a left join %s b 
                                                   on a.subject1_title=b.subject1_title and a.subject2_title=b.subject2_title and a.subject3_title=b.subject3_title and a.subject3_title=b.subject3_title where b.subject1_title is null
                                               """ %(options.subject4_table_name, options.textbook_table_name))
    
            print len(subjects4), 'subjects3 to be crawled yet'
            db.set_autocommit(False)
    
            for (subject1_title, subject2_title, subject3_title,subject4_title, subject4_url) in subjects4:
                print 'subject1_title:', subject1_title
                print 'subject2_title:', subject2_title
                print 'subject3_title:', subject3_title
                print 'subject4_title:', subject4_title
                print 'subject4_url:', subject4_url
                driver.get(subject4_url)
                time.sleep(3)
                crawl_textbook_listing(driver, db, workingdir, options, subject1_title, subject2_title, subject3_title, subject4_title)
                
                
        if options.crawl_textbook_details:
            textbooks = db.query("""select distinct subject1_title, subject2_title, subject3_title, subject4_title,textbook_title,textbook_url from %s where crawled=0""" %(options.textbook_table_name))
    
            print len(textbooks), 'textbooks yet to be crawled'
            db.set_autocommit(True)
    
            count = 0        
            for (subject1_title, subject2_title, subject3_title, subject4_title,textbook_title,textbook_url) in textbooks:
                count += 1
                print 'count:', count
                print 'textbook_title:',textbook_title
                print 'textbook_url:', textbook_url
                if not textbook_url:
                    continue    
                driver.get(textbook_url)
                time.sleep(3)
                format_journal= driver.find_elements_by_class_name("format-journal")
                if format_journal:
                    data={'crawled':None}
                    db.update(options.textbook_table_name, data, "textbook_url='%s'" %textbook_url)
                    time.sleep(3)
                    continue
                    #crawl_journal(driver,options,db,subject1_title, subject2_title, subject3_title, subject4_title,textbook_title,textbook_url)
                    #continue
                product_main = driver.find_elements_by_class_name("product-main")
                if not product_main:
                    data={'crawled':None}
                    db.update(options.textbook_table_name, data, "textbook_url='%s'" %textbook_url)
                    time.sleep(3)
                    continue
                productDetail_largeCover=product_main[0].find_element_by_class_name("productDetail-largeCover")
                coverImage = productDetail_largeCover.find_elements_by_tag_name('img')
                textbook_image_url = coverImage[0].get_attribute('src')
                print 'textbook_image_url:', textbook_image_url
                product_biblio = driver.find_element_by_class_name("product-biblio")

                productDetail_authorsMain=product_biblio.find_elements_by_class_name("productDetail-authorsMain")
                textbook_author=None
                if productDetail_authorsMain:
                  textbook_author = productDetail_authorsMain[0].text.strip()
                  if textbook_author.startswith('By '):
                      textbook_author = textbook_author[3:].strip()
                print 'textbook_author:', textbook_author
                textbook_publish_date=None
                textbook_copyright_year=None
                if product_biblio.find_elements_by_class_name("productDetail-dateImprint"):
                   textbook_publish_date = product_biblio.find_element_by_class_name("productDetail-dateImprint").text.strip(",")[0].strip()
                   textbook_publish_date= int(mx.DateTime.DateTimeFrom(textbook_publish_date))
                   productDetail_dateImprint=product_biblio.find_element_by_class_name("productDetail-dateImprint").text
                   if '©' in productDetail_dateImprint:
                      textbook_copyright_year = productDetail_dateImprint[(productDetail_dateImprint.find('©')+1):].strip()
                print 'textbook_publish_date:', textbook_publish_date
                print 'textbook_copyright_year:', textbook_copyright_year
                textbook_isbn = textbook_url[(textbook_url.find('-')+1):].replace(".html","").strip()
                if len(textbook_isbn)>12:
                   textbook_isbn = textbook_isbn.replace(textbook_isbn[textbook_isbn.find(','):],'').strip()
                textbook_isbn_10= textbook_isbn
                print 'textbook_isbn_10:', textbook_isbn_10
                productDetail_productCode = product_biblio.find_elements_by_class_name("productDetail-productCode")
                textbook_isbn_13=None
                if productDetail_productCode:
                    textbook_isbn_13=productDetail_productCode[0].text.replace('-','')
                    textbook_isbn_13=textbook_isbn_13.replace("ISBN:","").strip()
                else:
                    textbook_isbn_13=None
                print 'textbook_isbn_13:', textbook_isbn_13
                toc = 0
                toc_html = ''
                textbook_description=None
                textbook_publisher = "Wiley"
                print 'textbook_publisher:', textbook_publisher

                infoDescription = driver.find_elements_by_id("infoDescription")
                if infoDescription:           
                   #productDetail_richDataText = driver.find_elements_by_class_name("showMore")
                   #if productDetail_richDataText:
                   #    if productDetail_richDataText[0].text.strip() == 'See More':
                   #        productDetail_richDataText[0].click()
                
                   textbook_description = infoDescription[0].find_element_by_class_name("productDetail-richDataText")
                   textbook_description=textbook_description.get_attribute('innerText').strip()
                   print 'textbook_description:', textbook_description                        

                   
              
    #             ribbon_tab_navigation = driver.find_element_by_class_name("ribbon-tab-navigation")
    #             a = ribbon_tab_navigation.find_elements_by_xpath(".//li[@class = 'toc-tab']")
    #             if a:
    #                 toc = 1
    #                 print 'toc available'
    #                 #a[0].click()
    #                 #time.sleep(3)
    #             
                infoTableof = driver.find_elements_by_id("infoTableof")
                if infoTableof:
                    #if infoTableof[0].text.strip() == 'See More':
                    #    infoTableof[0].click()

                    content = infoTableof[0].find_element_by_class_name('productDetail-richDataText')
                    
                    toc_html = content.get_attribute('innerHTML').strip()
                    m = hashlib.md5()
                    m.update(textbook_url)
                    url_md5=m.hexdigest()
                    file = codecs.open(workingdir + '/wiley_toc_html/'+url_md5+'.html', "w", "utf-8")
                    file.write(toc_html)
                    file.close()
                    print 'TOC:'
                    print toc_html
                    print 'toc_html_file :',url_md5+'.html'
                    toc = 1    
                
                data = {'textbook_isbn':textbook_isbn_13, 'textbook_isbn_10':textbook_isbn_10,'textbook_isbn_13':textbook_isbn_13,
                            'textbook_author':textbook_author, 'textbook_copyright_year':textbook_copyright_year, 
                            'textbook_publish_date':textbook_publish_date, 'textbook_description':textbook_description, 
                            'textbook_publisher':textbook_publisher, 'textbook_image_url':textbook_image_url, 
                            'crawled':1, 'toc':toc, 'toc_html': toc_html}
                db.update(options.textbook_table_name, data, "textbook_url='%s'" %textbook_url)
                time.sleep(3)
                
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

def crawl_textbook_listing(driver, db, workingdir, options, subject1_title, subject2_title, subject3_title, subject4_title):
    page_num = 0
    index = 0
    while True:   
        page_num += 1
        browseListing = driver.find_element_by_id("browseListing")
        h2 = driver.find_element_by_xpath("//h2[@class='listing']")
        print h2.text
        for div in driver.find_elements_by_class_name("product-title"): #includes feature and browseListing
            index += 1
            print 'index:', index
            a = div.find_element_by_xpath('./a')
            textbook_title = a.text.strip()
            print 'textbook_title:', textbook_title
            textbook_url = a.get_attribute('href')
            print 'textbook_url:', textbook_url
            data = {'subject1_title':subject1_title, 'subject2_title':subject2_title, 'subject3_title':subject3_title, 'subject4_title':subject4_title, 'textbook_title':textbook_title, 'textbook_url':textbook_url}
            db.insert(options.textbook_table_name, data)
            
        paginator = driver.find_elements_by_xpath("//div[@class='paginator']")
        if not paginator:
           print 'paginator not exists'
           break
        paginator_selected = paginator[0].find_elements_by_class_name("paginator-selected")
        if not paginator_selected:
           print 'paginator-selected not exists'
           break
        next_siblings = paginator_selected[0].find_elements_by_xpath("./following-sibling::a[@class='paginator']")
        if not next_siblings:
           print 'paginator-selected following-sibling::a not exists'
           break           
        print 'move to next page', next_siblings[0].text
        next_siblings[0].click()
        time.sleep(3)
    db.commit()

def crawl_journal(driver,options,db,subject1_title, subject2_title, subject3_title, subject4_title,journal_title,journal_url):
    print "crawling journal"
    product_main = driver.find_element_by_class_name("product-main")
    productDetail_largeCover=product_main.find_element_by_class_name("productDetail-largeCover")
    coverImage = productDetail_largeCover.find_elements_by_tag_name('img')
    journal_image_url = coverImage[0].get_attribute('src')
    print 'journal_image_url:', journal_image_url
    product_biblio = driver.find_element_by_class_name("product-biblio")
    journal_author=None
    productDetail_volumeIssues=product_biblio.find_elements_by_tag_name("div")
    if productDetail_volumeIssues:
       journal_author=productDetail_volumeIssues[5].text.replace('Edited by:',"").strip()
    print "journal_author:",journal_author
    productDetail_productCode = product_biblio.find_elements_by_class_name("productDetail-productCode")
    journal_publisher="wiley"
    if productDetail_productCode:
       print_issn=productDetail_productCode[1].text
       print_issn=print_issn.replace("Print ISSN:","").replace("-","").strip()
    if productDetail_productCode:
       if "Online ISSN:" in print_issn:
           online_issn=print_issn
           print_issn=None
       else:
           online_issn=productDetail_productCode[2].text
    online_issn=online_issn.replace("Online ISSN:","").replace("-","").strip()
    print "print_issn:",print_issn
    print "online_issn:",online_issn 
    productDetail_society=product_biblio.find_elements_by_class_name("productDetail-society")
    if productDetail_society:
       journal_publisher=productDetail_society[0].text.strip()
    print "journal_publisher:",journal_publisher
    journal_description=None
    infoDescription = driver.find_elements_by_id("infoDescription")
    if infoDescription:
       journal_description = infoDescription[0].find_element_by_class_name("productDetail-richDataText")
       journal_description=journal_description.get_attribute('innerText').strip()
    print 'journal_description:', journal_description

 
    data = {'subject1_title':subject1_title, 'subject2_title':subject2_title, 'subject3_title':subject3_title,'subject4_title':subject4_title,'journal_title':journal_title,'journal_url':journal_url,'print_issn':print_issn,'online_issn':online_issn, 
                            'journal_author':journal_author,'journal_publisher':journal_publisher,'journal_image_url':journal_image_url,'journal_description':journal_description,
                            'crawled':1}


    db.insert(options.journal_table_name, data)    
    db.commit()
   
if __name__ == "__main__":
    Main()
