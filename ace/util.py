#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import sys
import time
import urllib
import MySQLdb
from bs4 import BeautifulSoup as bs
import csv
from urlparse import urlparse
import traceback
from random import randint
import mx.DateTime
import requests
from selenium import webdriver
import adconfig
  

#set mail id to send mails
def get_email_details():
    to='kend@vulcantechsoftware.com'
    cc='ssv@vulcantechsoftware.com'#,vvikram@vulcantechsoftware.com'
    #to = 'jordanbas@gmail.com'
    #cc = 'eyohay@gmail.com,vvikram@vulcantechsoftware.com,ssv@vulcantechsoftware.com,kend@vulcantechsoftware.com'
    return to, cc


#send mail
def send_mail(ad_type, num_urls_processed, starttime, endtime,ttime,filename, subject = '', msg = '', to = '', cc = ''):
    if not to and not cc:
        (to, cc) = get_email_details()
        #to=get_email_details()
        print to
        print cc
    if not subject:
        subject = 'Report on %s %s'%(ad_type,str(mx.DateTime.now().strftime("%Y-%m-%d %H:%M:%S")))
    if not msg:
        msg = "Report on %s details - %s\n%s\n%s\n%s\n%s"%(ad_type, str(mx.DateTime.now().strftime("%Y-%m-%d %H:%M:%S")), num_urls_processed, starttime, endtime, ttime)

    errno = 1
    if msg :
        try:
            if os.path.exists(filename):
                errno = os.system('echo "%s" | mutt -a "%s" -s "%s" -- %s "%s"'%(msg,filename, subject, to, cc))
        except:
            traceback.print_exc()
            pass
    




#create db conncetion
def cursor_define():
  db=MySQLdb.connect("localhost",adconfig.user,adconfig.passwd,adconfig.db,charset = 'utf8')
  db.autocommit(True)
  cursor = db.cursor()
  return cursor



# Inserting into tables.
def insert(domainid, urlid, link, srclink,inttime, table, cursor = None):
    time=str(mx.DateTime.now().strftime("%Y-%m-%d %H:%M:%S"))
    if not "http" in link:
       link=""
    try:
       tmp =urlparse(link)
    except:
       return
    advt_dom=tmp.netloc
    if len(advt_dom)==0:
       return
    if not cursor:
        cursor = cursor_define()
    print "Advertiser domain : ", advt_dom
    print "link : ",link
    try:
        sql = """insert into %s (domainid, urlid, advertiser,datetime,  advertiser_url, srclink,datetime_run) values ('%s', '%s', '%s', '%s', '%s','%s','%s')"""% (table, domainid, urlid, MySQLdb.escape_string(advt_dom),MySQLdb.escape_string(time), MySQLdb.escape_string(link),MySQLdb.escape_string(srclink),inttime)
        cursor.execute(sql)
        print "insert into table :",table
    except:
        traceback.print_exc()
        pass







#create csv file
def create_csvfile(sql,filename,cursor):
   try:
      
      cursor.execute(sql)
      result=cursor.fetchall()
      fd=open(filename,"wb")
      writer = csv.DictWriter(fd, fieldnames = ["src_domain","advertiser_domain","advertiser_per_domain"])
      writer.writeheader()
      c = csv.writer(fd)
      for row in result:
         c.writerow(row)
      fd.close()
   except:

      traceback.print_exc()
      cursor=cursor_define()
      create_csvfile(sql,filename,cursor)




