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
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

from bs4 import Comment

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
    cursor=db.get_cursor()
    try:
        if options.crawl_text:
            count=0
            attachments=db.query("select distinct url,attachment_id from %s where
             file_type = '%s' and landed=0 and url is not NULL"%(options.attachment_table,"URL Link"))
            print "Number of urls to crawl ",len(attachments)
            for (url,attachment_id,) in attachments:
                try:
                    count+=1
                    print "source url :",url
                    print "attachment_id :",attachment_id
                    print "count %s"%count
                    res=requests.get(url)
                    time.sleep(3)
                    
                    landing_url=res.url
                    if ".pdf" in landing_url:
                        raise Exception("Format not html")
                    data=res.text
                    soup=bs(data,"html")
                    iframes=soup.findAll("iframe")
                    num_of_iframs=len(iframes)
                    body=soup.find('body')
                    print body.text
                    [e.extract() for e in body.findAll('script')]
                    [e.extract() for e in body.findAll('style')]
                    comments = body.findAll(text=lambda text:isinstance(text, Comment))
                    [e.extract() for e in comments]
                    txt=body.text
                    visible_text=txt.replace('\n', ' ').replace('\s','').replace("  ",' ').replace('\t','')
                    
                    txt_location="/mnt/data/kendavar/orangegrove/textfile/%s.txt"%attachment_id
                    f=codecs.open(txt_location,"w","utf-8")
                    f.write(visible_text)
                    f.close()
                    print "txt_location :",txt_location
                    print "landing_url :",landing_url
                    print "num_of_iframs :",num_of_iframs
                    print "landing :",1
                    cursor.execute("""update %s set txt_location='%s',landing_url='%s',landed=%s,num_of_iframs=%s where attachment_id=%s"""%(options.attachment_table,txt_location,landing_url,1,num_of_iframs,attachment_id))
                except:
                    traceback.print_exc()
                    logging.exception('Got exception on main handler')
                    cursor.execute("""update %s set landing_url='%s', landed=%s where attachment_id=%s"""%(options.attachment_table,landing_url,-1,attachment_id))    
                    pass
                    #data={
                    #"txt_location":txt_location,
                    #"landing_url":landing_url,
                    #"num_of_iframs":num_of_iframs,
                    #"landed":1
                    #}
                    #db.update(options.attachment_table,data,"url='%s'"%url)
    except:
        traceback.print_exc()
        

        #data={"landed":-1}
        #db.update(options.attachment_table,data,"url='%s'"%url)


if __name__ == "__main__":
    Main()





