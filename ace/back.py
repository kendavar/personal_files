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
import re
import requests


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import logging
log_filename = './orangegrove.log'
logging.basicConfig(filename=log_filename,level=logging.DEBUG,)

logging.debug('This message should go to the log file')

from optparse import OptionParser




def Main():
    parser = OptionParser()
    parser.add_option("--crawl-text", dest="crawl_text", action="store_true", help="crawl text", default=False)
    parser.add_option("--working-dir", dest="workingdir", type="string", help="working directory", default='.')
    parser.add_option("--db-name", dest="db_name", type="string", help="database name", default='orangegrove')   
    parser.add_option("--attachment-table-name", dest="attachment_table", type="string", help="attachment table name", default='attachments')
    parser.add_option("--use-firefox", dest="use_firefox", action="store_true", help="use-firefox", default=True)
   
    (options, args) = parser.parse_args()    
    workingdir = options.workingdir.rstrip('/')
    num_of_iframs=0
    if not os.path.exists(workingdir):
        parser.error("workingdir not exists")
    db = mysql.DB(db=options.db_name)
    db.set_autocommit(True)
    try:
        display = None
        from pyvirtualdisplay import Display
        display = Display(visible=0, size=(1000,900))
        display.start()
    except:
        print 'No Xvfb!'

    driver = crawlutils.open_driver(use_firefox=options.use_firefox)
    try:
        if options.crawl_text:
            count=0
            attachments=db.query("select distinct url,attachment_id from %s where file_type = '%s' and landed=0 and url is not NULL"%(options.attachment_table,"URL Link"))
            print "Number of urls to crawl ",len(attachments)
            for (url,attachment_id,) in attachments:
                try:
                    count+=1
                    print "source url :",url
                    print "attachment_id :",attachment_id
                    print "count %s"%count
                    if "pdf" in url:
                        raise Exception(url)
                    driver.get(url)
                    iframes=driver.find_elements_by_tag_name("iframe")
                    body=driver.find_element_by_tag_name("body")
                    landing_url=driver.current_url
                    if "pdf" in landing_url:
                        raise Exception(landing_url)
                
                    cursor=db.get_cursor()
                    visible_text=body.text
                    if iframes:
                        num_of_iframs=len(iframes)
                        print "landing_url :",landing_url
                        print"landed :",2
                        print"num_of_iframs :",num_of_iframs
                        #data={
                        #"landing_url":landing_url,
                        #"landed":2,
                        #"num_of_iframs":num_of_iframs
                        #}
                        
                        cursor.execute("""update %s set landing_url='%s',landed=%s,num_of_iframs=%s  where url='%s'"""%(options.attachment_table,landing_url,2,num_of_iframs,url))
                        #db.update(options.attachment_table,data,"url='%s'"%url)
                    else:
                        txt_location="/mnt/data/kendavar/orangegrove/textfile/%s.html"%attachment_id
                        f=codecs.open(txt_location,"w","utf-8")
                        f.write(visible_text)
                        f.close()
                        print "txt_location :",txt_location
                        print "landing_url :",landing_url
                        print "num_of_iframs :",num_of_iframs
                        print "landing :",1
                        cursor.execute("""update %s set txt_location='%s',landing_url='%s',landed=%s,num_of_iframs=%s where url='%s'"""%(options.attachment_table,txt_location,landing_url,1,num_of_iframs,url))
                except:
                    traceback.print_exc()
                    logging.exception('Got exception on main handler')
                    cursor.execute("""update %s set landed=%s where url='%s'"""%(options.attachment_table,-1,url))    
                    pass


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

from src import mysql
from src import crawlutils
import shutil
from selenium import webdriver

db = mysql.DB("usgs")
links = db.query("""select document_id,link from %s where crawled=2""" %("usgs"))
driver=webdriver.Chrome()
driver.set_window_size(1000,900)
for (document_id,link,) in links:
    txt_location="/mnt/data/kendavar/usgs/txtfiles/%s_txt"%document_id
    filename="/mnt/data/kendavar/usgs/screenshots/%s.png"%document_id
    driver.save_screenshot(filename)
    crawlutils.resize_png_image(filename)
    img_location="/mnt/data/kendavar/usgs/screenshot_png/%s_png"%document_id
    shutil.copyfile(filename,img_location)
    data = {
    'screenshot':img_location,
    'txt_location':txt_location,
    'crawled':1
    }
    db.update("usgs", data, "document_id='%s'" %document_id)

update usgs set crawled=2 where document_id="0df6067dcbbea9cb4c42c918880fd17a";
update usgs set crawled=2 where document_id="1dc0a0b4aca70b42b61b7fb30fb0807d";
update usgs set crawled=2 where document_id="2c8146a8c429e16ac06abe27433690bb";
update usgs set crawled=2 where document_id="63476d7287f04e063e35be37e2c07c0f";
update usgs set crawled=2 where document_id="6ef92bbdc5eedc52fc6f45cfeda71ad8";
update usgs set crawled=2 where document_id="82ca99b0535da277e14953d01ccb8f62";
update usgs set crawled=2 where document_id="b5856e443e3719b367d602372fde87be";
update usgs set crawled=2 where document_id="bc5ae3d0135834d9f0607f0e6a7ed69c";
update usgs set crawled=2 where document_id="fa6e196b406184d3205db10ea82db86c";
update usgs set crawled=2 where document_id="fb15c53cf3520f54ad8adbf01de4a776";



update toc set pdf_link="http://open.lib.umn.edu/businesscommunication/open/download?filename=Business-Communication-for-Success-1450464413&type=pdf" where document_id="d0ee8bc8c084a35584cdea597b79bb66";
update toc set pdf_link="http://open.lib.umn.edu/collegesuccess/open/download?filename=College-Success-1450716685&type=pdf" where document_id="09866c3b3802b01e01a2b0e79e94a40a";
update toc set pdf_link="http://open.lib.umn.edu/criminallaw/open/download?filename=Criminal-Law-1450391163&type=pdf" where document_id="3536e8d2c35ff5403a3da41276125c86";
update toc set pdf_link="http://www.cali.org/sites/default/files/FedRulesAppPro.pdf" where document_id="813d3a0c5d6f9fe63523e70777c90b51";
update toc set pdf_link="http://www.cali.org/sites/default/files/FRCP_LII_0.pdf" where document_id="783173eb90b2ddc6b411bab54b071e64";
update toc set pdf_link="http://www.cali.org/sites/default/files/FRCrimPro_LII_0.pdf" where document_id="a89b1d574ba10f83df6356db9492f95f";
update toc set pdf_link="http://www.cali.org/sites/default/files/FRE_LII_0.pdf" where document_id="ca5b548fc40c20771c37e7974d44ecd5";
update toc set pdf_link="http://www.cali.org/sites/default/files/usc17%40113-126.pdf" where document_id="e4ea9c4f5d525853c535bb343bf323fc";
update toc set pdf_link="http://www.cali.org/sites/default/files/Title35Patents_Aug2014.epub" where document_id="2f20216e500592d82d5a0cf4efe606d5";
update toc set pdf_link="http://www.cali.org/sites/default/files/Trademarks.pdf" where document_id="1717c9778fa3df4ff78dd403d194ca79";
update toc set pdf_link="http://open.lib.umn.edu/infostrategies/open/download?filename=Information-Strategies-for-Communicators-1445907114&type=pdf" where document_id="1787f1c401959e9e4bfa51ed134c0daa";
update toc set pdf_link="http://open.lib.umn.edu/principlesmanagement/open/download?filename=Principles-of-Management-1445970412&type=pdf" where document_id="4025f9d4b28b5702275fd5d1c5b349cc";
update toc set pdf_link="http://open.lib.umn.edu/principlesmarketing/open/download?filename=Principles-of-Marketing-1445970501&type=pdf" where document_id="7469f427eed46e7cb2d0bee08ae804ab";
update toc set pdf_link="http://www.saylor.org/site/textbooks/Information%20Systems%20for%20Business%20and%20Beyond.pdf" where document_id="f6f99fd503f27dbbafa684f7de27e244";
update toc set pdf_link="http://open.lib.umn.edu/informationsystems/open/download?filename=Information-Systems-A-Manager039s-Guide-to-Harness-Technology-1445970326&type=pdf" where document_id="81c75da6163eb9a372f75817e107f1d3";
update toc set pdf_link="http://open.lib.umn.edu/writingforsuccess/open/download?filename=Writing-for-Success-1445970582&type=pdf" where document_id="6bfd5a798bc16f81d35016eabdb4a3ec";
update toc set pdf_link="https://drive.google.com/uc?export=download&id=0By7BMGeZI-NUNDYydjR1WFNMVmc" where document_id="1aee7475f40f615ad67cc2d2112b33db";
update toc set pdf_link="http://dc.uwm.edu/cgi/viewcontent.cgi?article=1002&context=biosci_facbooks_bergtrom" where document_id="e3661153ee999fcfa7b5e9e7b7ae24f5";
update toc set pdf_link="http://open.lib.umn.edu/intropsyc/open/download?filename=Introduction-to-Psychology-1445970204&type=pdf" where document_id="f8bbb8d68b9e97878dcd46b95e3c9bc2";
update toc set pdf_link="http://open.lib.umn.edu/socialpsychology/open/download?filename=Principles-of-Social-Psychology-1445970048&type=pdf" where document_id="b97a8f429ebf66c976143fe1dfbc9d5d";
update toc set pdf_link="http://textbooks.opensuny.org/download/nursing-care-at-the-end-of-life/" where document_id="a455ab5625dbc9af9ecbc0aa928c3002";
update toc set pdf_link="http://www.cali.org/sites/default/files/FedRulesBankrupctyPro.pdf" where document_id="3eaebb19f1cf6610a284d70c06c7c09e";







update toc set toc=4 where document_id="ecfb41ea83d934fe57aa4ef266c24d7c"; 
update toc set toc=4 where document_id="47b74ecd00e2a37a05847e30adff11bb"; 
update toc set toc=4 where document_id="86cbe9c53a753d65281c76de6f6c1ed3"; 











