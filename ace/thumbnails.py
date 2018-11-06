#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
import time
import os
import traceback
import codecs
import re
from datetime import datetime
import shutil

import crawlutils
from optparse import OptionParser

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import TimeoutException
try:
    import boto.s3
    import boto.s3
    import boto.s3.connection
    import boto.s3.bucket
    import boto.s3.key 
except:
    print 'boto not found!'
    pass

def main():
    parser = OptionParser()
    parser.add_option("--url-file", dest="url_file", type="string", help="file name where document_id and document_url found as tab separated values")
    parser.add_option("--working-dir", dest="workingdir", type="string", help="working directory", default='.')
    parser.add_option("--skip", dest="skip", type=int, help="integer value", default=0)
    parser.add_option("--s3bucket", dest="s3bucket", type="string", help="s3bucket name")
    parser.add_option("--use-login", dest="use_login",  type="string", help="login website (eg. pearson, wgu, iwu, etc.,)")
    (options, args) = parser.parse_args()
    
    if not options.url_file:
        parser.error("--url-file REQUIRED")
    
    workingdir = options.workingdir.rstrip('/')
    
    if not os.path.exists(workingdir):
        parser.error("workingdir not exists")
    
    url_file = None
    if os.path.exists(options.url_file):
        url_file = options.url_file
    elif os.path.exists(options.workingdir + '/' + options.url_file):
        url_file = options.workingdir + '/' + options.url_file
    else:
        print 'file not exists:', options.url_file
        return
        
    documents = []
    f = open(url_file, 'r')
     
    for l in f:
        items = l.strip().split('\t')
        if len(items) != 2:
            continue
        (document_id, document_url) = items
         
        if len(document_id) != 32:
            continue
             
        if not (document_url.startswith('http://') or document_url.startswith('https://')):
            continue
          
        documents.append((document_id, document_url))
         
 
    print len(documents), 'document urls to be processed'
    if len(documents) > 0:
        login = None
        if options.use_login:
            if options.use_login == 'pearson':
                login_url = 'http://portal.mypearson.com/mypearson-login.jsp'
                login = { 'login_url':login_url,
                               'username-control-id':'loginname-id',
                               'password-control-id':'password-id',
                               'username':'',
                               'password':''
                             }
            else:
                parser.error("--use-login=" + options.use_login + " not supported yet")
        s3bucket = None
        if options.s3bucket :
            s3bucket = gets3bucket(bucket_name=options.s3bucket)
        create_thumbnails(documents=documents, workingdir=options.workingdir, skip=options.skip, login=login, s3bucket=s3bucket)

def gets3bucket(bucket_name):
    try:        
        AWS_ACCESS_KEY_ID = ''
        AWS_SECRET_ACCESS_KEY = ''
        
        s3conn = boto.s3.connection.S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
        bucket = boto.s3.bucket.Bucket(s3conn, bucket_name)
        return bucket
    except:
        traceback.print_exc()
         
def create_thumbnails(documents, workingdir='.', skip=0, login=None, s3bucket=None):
    try:
        display = None
        from pyvirtualdisplay import Display
        display = Display(visible=0, size=(1280, 1024))
        display.start()
    except:
        print 'No Xvfb!'

    workingdir = workingdir.rstrip('/')
    print 'workingdir:', workingdir 
        
    if not os.path.exists(workingdir):
        parser.error("workingdir not exists")
        
    thumbnail_folder = workingdir + "/thumbnails/"
    if not os.path.exists(thumbnail_folder):
        os.mkdir(thumbnail_folder)
        
    thumbnail_doubts_folder = workingdir + "/thumbnails_doubts/"
    if not os.path.exists(thumbnail_doubts_folder):
        os.mkdir(thumbnail_doubts_folder)
        
    if skip:
        print 'skip:', skip
        
    log_file = codecs.open(workingdir + '/error_log.txt', 'a', 'utf-8')
    
    file(workingdir + '/running_status.txt', 'w').write("crawling started")
    
    if os.path.exists(workingdir + '/running_firefox_pid.txt'): os.remove(workingdir + '/running_firefox_pid.txt')
    
    driver, browser_pid = crawlutils.open_driver()
    try:
        if browser_pid:
            file(workingdir + '/running_firefox_pid.txt', 'w').write("%s"%(browser_pid))
        
        #crawlutils.login(driver, login_url, 'loginname-id', 'password-id', 'alc_acc', 'n0thinghaschanged')
        if login:
            print 'login_url:', login['login_url']
            crawlutils.login(driver, login['login_url'], login['username-control-id'], login['password-control-id'], login['username'], login['password'])
        
        print len(documents), 'to be processed'
        
        count = 0
        for (document_id,document_url)  in documents:
            count += 1
            if skip > count: continue
            print 'count:', count
            try:
                file(workingdir + '/running_status.txt', 'w').write("%s\t%s\t%s"%(count, document_id, document_url))
                create_thumbnail(driver, workingdir, document_id, document_url, s3bucket)                
            except:
                traceback.print_exc()
                if driver :
                    try: driver.quit()
                    except:pass                              
                if os.path.exists(workingdir + '/running_firefox_pid.txt'): os.remove(workingdir + '/running_firefox_pid.txt')
                driver, browser_pid = crawlutils.open_driver()                
                if browser_pid:
                    print 'browser_pid:', browser_pid
                    file(workingdir + '/running_firefox_pid.txt', 'w').write("%s"%(browser_pid))
                 
                if login:
                    print 'login_url:', login['login_url']
                    crawlutils.login(driver, login['login_url'], login['username-control-id'], login['password-control-id'], login['username'], login['password'])
                time.sleep(5)
                
        print 'completed'
    except:
        traceback.print_exc()
    finally:
        if os.path.exists(workingdir + '/running_firefox_pid.txt'): os.remove(workingdir + '/running_firefox_pid.txt')
        if os.path.exists(workingdir + '/running_status.txt'): os.remove(workingdir + '/running_status.txt')
        try: driver.quit()
        except:pass
        del driver
        if display: display.stop()
        log_file.close()
        
def create_thumbnail(driver, workingdir, document_id, document_url, s3bucket=None):
    print 'document_id:', document_id                   
    print document_url
    
    thumbnail_name = "%s_png" %(document_id)
    thumbnail_local_filepath = workingdir + "/thumbnails/" + thumbnail_name
    thumbnail_local_filepath_doubts = workingdir + "/thumbnails_doubts/" + thumbnail_name

    if os.path.exists(thumbnail_local_filepath):
        print 'local copy of the thumbnail exists'
    elif os.path.exists(thumbnail_local_filepath_doubts):
        print 'local copy of the thumbnail exists on doubts folder'
        thumbnail_local_filepath = None
    else:
        if "media.pearsoncmg.com" in document_url :
            driver.set_window_size(900, 800)
        elif "khanacademy.org" in document_url :
            driver.set_window_size(1280, 1024)
        driver.get(document_url)
        time.sleep(3)
        crawlutils.handle_alert(driver)
        title = driver.title
        print 'Title:', title        
        file(workingdir + '/document_tiles.txt', 'a').write("%s\t%s\n"%(document_id, title))
        title = title.lower()
        if 'log in' in title or 'sign in' in title or '404' in title or 'expired' in title or 'not found' in title :
            print '404 page:', document_id, ">>", driver.current_url
            file(workingdir + '/loaded_different_url.txt', 'a').write("%s\t%s"%(document_id, document_url))
            driver.switch_to_window(driver.window_handles[-1])
            driver.save_screenshot(thumbnail_local_filepath_doubts)  
            close_all_new_windows(driver)
            print 'screenshot done'         
            time.sleep(1)           
            if not os.path.exists(thumbnail_local_filepath_doubts):
                thumbnail_local_filepath_doubts = None        
            thumbnail_local_filepath = None          
        else:
            retry = 0
            while True:
                if retry > 3: break
                time.sleep(30)
                driver.switch_to_window(driver.window_handles[0])            
                driver.save_screenshot(thumbnail_local_filepath)
                close_all_new_windows(driver)
                print 'screenshot done'         
                if os.path.exists(thumbnail_local_filepath):
                    thumbnail_size = os.stat(thumbnail_local_filepath).st_size
                    if thumbnail_size < 10000:
                        #print 'file size is small.(%s Bytes) so moving to doubts folder' %thumbnail_size
                        #shutil.move(thumbnail_local_filepath, thumbnail_local_filepath_doubts)
                        #thumbnail_local_filepath = None
                        print 'file size is small.(%s Bytes) so retrying' %thumbnail_size
                        retry +=1
                        continue
                break
                        
            else:
                thumbnail_local_filepath = None

    if thumbnail_local_filepath :
        if os.path.exists(thumbnail_local_filepath):
            thumbnail_size = os.stat(thumbnail_local_filepath).st_size
            if thumbnail_size > 10000:
                crawlutils.resize_png_image(thumbnail_local_filepath)
                print 'thumbnail resized'     
                               
    if thumbnail_local_filepath_doubts :
        if os.path.exists(thumbnail_local_filepath_doubts):
            thumbnail_size = os.stat(thumbnail_local_filepath_doubts).st_size
            if thumbnail_size > 10000:
                crawlutils.resize_png_image(thumbnail_local_filepath_doubts)
                print 'thumbnail resized'                    
        
    if thumbnail_local_filepath:
        upload_thumbnail_to_s3(s3bucket, thumbnail_name, thumbnail_local_filepath)
        
        
def close_all_new_windows(driver):
    while len(driver.window_handles) > 1:
        driver.switch_to_window(driver.window_handles[-1])
        driver.close()
    driver.switch_to_window(driver.window_handles[0])    
        
        
def upload_thumbnail_to_s3(s3bucket, thumbnail_name, thumbnail_local_filepath):    
    if s3bucket:
        print 's3 put', thumbnail_local_filepath
        if thumbnail_local_filepath:
            if os.path.exists(thumbnail_local_filepath) :
                k = boto.s3.key.Key(s3bucket)
                k.key = thumbnail_name
                k.set_metadata('Content-Type', 'image/png')
                k.set_contents_from_filename(thumbnail_local_filepath)
                del k
                print 'image uploaded into s3'
                
                
if __name__=='__main__':
    main()
