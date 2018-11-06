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

def main():
    parser = OptionParser()
    parser.add_option("--url-file", dest="url_file", type="string", help="file name where document_id and document_url found as tab separated values")
    parser.add_option("--working-dir", dest="workingdir", type="string", help="working directory", default='.')
    parser.add_option("--skip", dest="skip", type=int, help="integer value", default=0)
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



def create_thumbnails()
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
    log_file = codecs.open(workingdir + '/error_log.txt', 'a', 'utf-8')
        
