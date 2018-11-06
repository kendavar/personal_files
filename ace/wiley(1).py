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
#import MySQLdb
import socket
import time
import crawlutils

import optparse
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from bs4 import BeautifulSoup as bs
reload(sys)
sys.setdefaultencoding("utf-8")
#conn = MySQLdb.Connection(db='wiley_sept29', host='localhost', user='aceuser', passwd='aceuser', port=3306, use_unicode=True,charset = 'utf8')
#conn.autocommit(True)
#cursor = conn.cursor()

def db(sql,row):
    try:
       cursor.execute(sql,(row))
       conn.commit()
    except:
       conn.rollback()
def csv(table,rows):
    try:
       out = open(table, 'w')
       for row in rows:
          for column in row:
             out.write('%d;' % column.encode('utf-8'))
             out.write('\n')
       out.close()
    except Exception as e:
        print e
        pass

   



def main():
   subject1=[]
   subject2=[]
   textbook=[]
   try:
       driver=webdriver.Chrome()
       loginurl = "http://www.wiley.com/WileyCDA/Section/id-404420.html"
       driver.get(loginurl)
       time.sleep(5)
       WebDriverWait(driver, 10).until(lambda s: s.find_element_by_class_name('subjects-hoverlist').is_displayed())
       ui=driver.find_element_by_class_name('subjects-hoverlist')
       a_tag=ui.find_elements_by_tag_name('a')
       for i in a_tag:
           sub1=i.text
           url1=i.get_attribute('href')
           sub=[sub1,url1]
           subject1.append(sub)
           print i.get_attribute('href')
           print subject1 
           #sql="insert into subject2_wiley values(%s,%s)"
           #row=(sub1,url1)
           #db(sql,row)   
           driver.get(i.get_attribute('href'))
           time.sleep(10)
           WebDriverWait(driver, 10).until(lambda s: s.find_element_by_class_name('subjects').is_displayed()) 
           ui1=driver.find_element_by_class_name('subjects')
           a_tag2=ui1.find_elements_by_tag_name('a')
           for i2 in a_tag2:
               sub2=i2.text
               url2=i2.get_attribute('href')
               sub=[sub1,sub2,url2]
               subject2.append(sub)
               print i2.get_attribute('href')
               print i2.text
               #sql="insert into subject2_wiley values(%s,%s,%s)"
               #row=(sub1,sub2,url2)
               #db(sql,row)
               driver.get(i2.get_attribute('href'))
               time.sleep(10) 
               div=driver.find_element_by_id('main-content-left')
               div1=div.find_element_by_id('browseListing')
               WebDriverWait(driver, 25).until(lambda s: s.find_elements_by_class_name('product-title'))
               div2=div1.find_elements_by_class_name('product-title')
               print "done",div2
               for a in div2:
                   a_tag3=a.find_element_by_tag_name('a')
                   print a_tag3
                   url3=a_tag3.get_attribute('href')
                   sub3=a_tag3.text
                   sub=[sub1,sub2,sub3,url3]
                   textbook.append(sub)
                   #sql="insert into textbook_wiley values(%s,%s,%s,%s)"
                   #row=(sub1,sub2,sub3,url2)
                   #db(sql,row)   
                   print textbook
                   csv('subject1.csv',subject1)
                   csv('subject2.csv',subject2)
                   csv('textbook.csv',textbook)
                   driver.close()
                   sys.exit()       
       print sub1[0]
       print sub2[0]
       print url1[0]
       print url2[0]
       #cursor.execute(sql,(row))
       #db.commit()
       driver.close()
       conn.close()
   except Exception as e:
      print e
      driver.close()
   

if __name__ == '__main__':
    main()
