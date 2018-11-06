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
import configoer
import MySQLdb
import socket
import time

import optparse
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from bs4 import BeautifulSoup as bs
reload(sys)
sys.setdefaultencoding("utf-8")


class oer:
    #initailize all values
    element_name=[]
    j=-1
    element_value=[]
    title=None
    link=None
    img_src=None
    description=None
    columns_table=[]
    insert_values=[]
    columns=[]
    keyword=""
    in_values=[]
    table=""
    Material_Type=None
    Provider=None
    Provider_Set=None
    Subject=None
    Author=None
    seq_num=0
    #Make a connection to local machine
    db = MySQLdb.connect("localhost",configoer.USER,configoer.PASS,"oer",charset = 'utf8')                #host="192.168.1.37",port=3306,user="root",passwd="password",db="oer", charset = 'utf8')
    #logged to file
    logging.basicConfig(filename='oer.log',filemode='w',level=logging.DEBUG)
    #socket created
    #client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #create cursor object
    cursor = db.cursor()

    def __init__(self,table):
       try:
          self.table=table
          print "oer object created"
          #self.client_socket.connect(('localhost', 42937))
          #print dir(self.client_socket)
       except:
          print "Erro while initialing"
          #logging.debug(self.client_socket.connect(('localhost', 42937)))
          #logging.warning(self.client_socket.connect(('localhost', 42937)))

    #connect to database 
    def database_connect(self):
        try:
           self.db = MySQLdb.connect("localhost",configoer.USER,configoer.PASS,"oer",charset = 'utf8' )
           self.cursor = self.db.cursor()
           return 
        except Exception as e:
           print "Error connecting to database : ",e
    
    #query are executed and commited and excetions are handled here
    def database_query(self,sql):
        try:
           self.cursor.execute(sql)
           self.db.commit()
        except Exception as e:
           logging.debug(self.cursor.execute(sql))
           #table doesn't exits
           if e.args[0] == 1146:
              self.create_table()
              self.database_query()
           elif e.args[0] == 1050:#while droping table if table exits
              print "Table exits"
              self.drop_table(self)
           elif e.args[0] == 1136:#column count does not match
              print sql
              sys.exit()
           elif arg[0]==2006 or arg[0]==2002:#mysql server has gone away or Can't connect to local MySQL server through socket
               self.database_connect()
           else:
              self.db.rollback()
              print sql
              print "Error in excuting query : ",e
              sys.exit()
       
    #fetch keywords from the table keywords     
    def keywords(self):
       try:
          sql="select keyword from keywords"
          self.cursor.execute(sql)
          self.db.commit()
          #self.database_query(sql)
          results = self.cursor.fetchall() 
          self.keyword=""
          for result in results:
             self.keyword=result[0]
             self.open_url()
          print "Completed inserting"
       except Exception as e:
          logging.debug(e)
          print "Error in Keywords : ",e 

    #url is opened and soup object is created
    def open_url(self):
        try:
           f = { "batch_size" : "100","sort_by" : "search","view_.mode" : "summary","f.search" : self.keyword }
           url= "https://www.oercommons.org/search?" + urllib.urlencode(f)
           headers = {'User-Agent': 'Mozilla/5.0'}
           response = requests.get(url, headers=headers,timeout=5)
           time.sleep(5)
           soup=bs(response.text)
           self.crawl_data(soup)
        except requests.exceptions.Timeout as e:
           # Maybe set up for a retry, or continue in a retry loop
           print "time out"
           logging.debug(e)
           self.open_url()
        except requests.exceptions.TooManyRedirects as e:
            print "Bad url"
            # Tell the user their URL was bad and try a different one
            logging.debug(e,'Bad url:',url)
            sys.exit(1)
       
        except Exception as e:
           print "Error in opn_url : ",e
           logging.debug(e)
           
        
    #crawl all the data from each keywords
    def crawl_data(self,soup):
        try: 
           self.seq_num=0
           for i,tag in enumerate(soup.find_all('article')): 
               self.title=None
               self.link=None
               self.img_src=None
               self.description=None
               self.Material_Type=None
               self.Provider=None
               self.Provider_Set=None
               self.Subject=None
               self.Author=None 
               self.seq_num=1+i            
               if tag['data-index-position']!="":
                  #self.keyword.append(keyword)
                  self.img_src=(tag.img['src'])
                  self.link=(tag.a['href'])
                  self.title=tag.a.text#.encode('utf-8')
                  for des in tag.find_all('p'):
                     if des['class'][0]=='abstract-full':
                        des.a.extract()
                        self.description=des.text.strip()#.encode('ascii', 'xmlcharrefreplace')##.encode('utf-8'))
                  for ele in tag.find_all('dt'):
                     #element_name.append(ele.text.strip(':'))#.encode('utf-8'))
                     if ele.text.strip(':') not in self.columns:
                          self.columns.append(ele.text.strip(':'))
                  for item in tag.dl.findAll('dd'):
                     ele=item.find_previous_sibling('dt').text.strip(':').strip()
                     #print ele,item
                     if ele == "Material Type" and self.Material_Type !=None:
                         self.Material_Type=self.Material_Type + ", "+item.text.strip()
                         #print self.Material_Type
                     elif ele == "Material Type":
                         self.Material_Type=item.text.strip()
                         #print self.Material_Type
                     if ele == "Provider" and self.Provider !=None:
                         self.Provider=self.Provider+", "+item.text.strip()
                     elif ele == "Provider":
                         self.Provider=item.text.strip()
                     if ele == "Provider Set" and self.Provider_Set !=None:
                         self.Provider_Set=self.Provider_Set+", "+item.text.strip()
                     elif ele == "Provider Set":
                         self.Provider_Set=item.text.strip()
                     if ele == "Subject" and self.Subject !=None:
                         self.Subject=self.Subject+", "+item.text.strip()
                     elif ele == "Subject":
                         self.Subject=item.text.strip()
                     if ele == "Author" and self.Author!=None:
                         self.Author=self.Author+", "+item.text.strip() 
                     elif ele == "Author":
                         self.Author=item.text.strip() 
   
                  self.insert_table()
               else:
                  self.insert_table()
        except Exception as e:
            print "Error in crawlig data : ",e
            logging.error("crawling_data",e.message)
            sys.exit()

    def drop_table(self):
         try:
            self.database_query("DROP TABLE IF EXISTS "+self.table)
            print self.table+" Droped"
         except Exception as e:
             print "Error in drop_table ",e.message

    def create_table(self):
       try:
          sql_string=""
          for column in self.columns:
             sql_string=sql_string+column.replace(" ","_")+' varchar(200),'
          sql="create table IF NOT EXISTS oercommons(_id serial primary key,keyword varchar(255),title varchar(255),link varchar(512),image varchar(512),description text,Material_Type varchar(200),Provider varchar(200),Provider_Set varchar(200),Subject varchar(200),Author varchar(200),seq_num int default NULL) DEFAULT CHARSET=utf8"
          self.database_query(sql)
          print "Table created"
       except Exception as e:
           print "Error while creating the table",e
           sys.exit()

    #insert into table
    def insert_table(self):
        try:    
            sql="""insert into oercommons(keyword,title,link,image,description,Material_Type,Provider,Provider_Set,Subject, Author,seq_num) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            row=(self.keyword,self.title,self.link,self.img_src,self.description,self.Material_Type,self.Provider,self.Provider_Set,self.Subject,self.Author,self.seq_num)
            self.cursor.execute(sql,(row))
            self.db.commit()
            print self.keyword+" " + self.title+" inserted"
        except Exception as e:
           logging.debug(self.cursor.execute(sql))
           #table doesn't exits
           if e.args[0] == 1146:
              self.create_table()
              self.database_query()
           elif e.args[0] == 1050:#while droping table if table exits
              print "Table exits"
              self.drop_table(self)
           elif e.args[0] == 1136:#column count does not match
              print sql
              sys.exit()
           else:
              self.db.rollback()
              print sql
              print "Error in excuting query : ",e
              sys.exit()

    #delete all the contents in the table
    def delete_table(self):
        sql="delete from oercommons"
        self.database_query(sql)
        print "All rows deleted "+self.table

    def fetch_land_url(self):
        try:
           sql="select link,document_id,landing_url from oercommons limit 2"
           self.cursor.execute(sql)
           #self.database_query(sql)
           results = self.cursor.fetchall() 
           print results
           for result in results:
              if not None == result[0]:
                 if not None == result[1]:
                    if None == result[2]: 
                       self.url=result[0]
                       self.doc_id=result[1]
                       self.land_url()
                    else:
                       print "Landing url is already present:",result[2]
                 else:
                     print "Document_id is not found"
              else:
                  print "URL is not found"
           print "Completed inserting"
        except Exception as e:
           logging.error(e)
           print "Error in fetching link",e
    
    def sel_chrome(self):
        self.driver=webdriver.Chrome()
    
    def land_url(self):
        try:
            self.driver.get(self.url)
            time.sleep(5)
            WebDriverWait(self.driver, 10).until(lambda s: s.find_element_by_id('goto').is_displayed())
            self.driver.find_element_by_id('goto').click() 
            time.sleep(5)
            WebDriverWait(self.driver, 10).until(lambda s: s.find_element_by_id('resource').is_displayed())
            landing_url=self.driver.find_element_by_id('resource').get_attribute('src')
            #print landing_url
            self.driver.switch_to.frame(self.driver.find_element_by_id('resource'))
            land_text=self.driver.find_element_by_tag_name('body').text
            #print land_text
            file('/home/vulcantech/kendavar/Ace/oercommon/'+self.doc_id+'.txt','w').write(land_text)
            sql="update oercommons set landing_url =%s where document_id=%s"
            logging.debug(self.cursor.execute(sql,(landing_url,self.doc_id)))
            self.cursor.execute(sql,(landing_url,self.doc_id))
            self.db.commit
            print "insert landing url",landing_url
            sys.exit()
        except TimeoutException as e:
            print "body not found",e
            logging.error(e)
            return
            #continue
        except MySQLdb.Error as e:
            logging.error(e) 
  
    def print_all(self):
        print len(self.columns_table)
        print len(self.in_values)
        print self.j


    #close the connection   
    def __del__(self):
        self.db.close()
        self.driver.close()
        print "destroyed"


def main():
   parser = optparse.OptionParser()
   #parser.add_option('-a', action="store_true", default=False)
   parser.add_option('-t', action="store", dest="table",help="Enter the table name")
   parser.add_option('-l', action="store", dest="land_url", help="fetch the landing url enter true")
   parser.add_option('-k', action="store", dest="keyword", help="fetch the keyword data enter true")
   options, remainder = parser.parse_args()
   if options.table:
       obj=oer(options.table)
   if options.land_url:
       obj.sel_chrome()
       obj.fetch_land_url()
   #ob.delete_table()
   if options.keyword:
       obj.keywords()
   #ob.create_table()
   

if __name__ == '__main__':
    main()
    
