import codecs
import subprocess
import getpass
import re
import os
import traceback
import urllib
import urllib2
import cookielib
import time
import shutil
from PIL import Image
import StringIO

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import TimeoutException

def open_firefox(download_dir=None):
    prev_firefox_pids = get_all_firefox_pids()
    profile = webdriver.FirefoxProfile()
    if download_dir:
        handlers = ['application/pdf', 'application/vnd.pdf', 'text/pdf',
                            'application/msword',
                            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                            'application/vnd.openxmlformats-officedocument.wordprocessingml.template',
                            'application/vnd.ms-word.document.macroEnabled.12',
                            'application/vnd.ms-word.template.macroEnabled.12',
                            'application/vnd.ms-excel',
                            'application/vnd.ms-excel',
                            'application/vnd.ms-excel',
                            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                            'application/vnd.openxmlformats-officedocument.spreadsheetml.template',
                            'application/vnd.ms-excel.sheet.macroEnabled.12',
                            'application/vnd.ms-excel.template.macroEnabled.12',
                            'application/vnd.ms-excel.addin.macroEnabled.12',
                            'application/vnd.ms-excel.sheet.binary.macroEnabled.12',
                            'application/vnd.ms-powerpoint',
                            'application/vnd.ms-powerpoint',
                            'application/vnd.ms-powerpoint',
                            'application/vnd.ms-powerpoint',
                            'application/vnd.openxmlformats-officedocument.presentationml.presentation',
                            'application/vnd.openxmlformats-officedocument.presentationml.template',
                            'application/vnd.openxmlformats-officedocument.presentationml.slideshow',
                            'application/vnd.ms-powerpoint.addin.macroEnabled.12',
                            'application/vnd.ms-powerpoint.presentation.macroEnabled.12',
                            'application/vnd.ms-powerpoint.template.macroEnabled.12',
                            'application/vnd.ms-powerpoint.slideshow.macroEnabled.12'
                            ]

        profile.set_preference("browser.download.folderList",2)
        profile.set_preference("browser.download.manager.showWhenStarting",False)
        profile.set_preference("browser.download.dir", download_dir)
        profile.set_preference("browser.download.downloadDir", download_dir)
        profile.set_preference("browser.download.defaultFolder", download_dir)
        profile.set_preference("browser.helperApps.alwaysAsk.force", False)
        profile.set_preference("browser.helperApps.neverAsk.saveToDisk", ",".join(handlers))
        profile.update_preferences()
    driver = webdriver.Firefox(firefox_profile=profile)
    current_firefox_pids = get_all_firefox_pids()
    new_firefox_pids = list(set(current_firefox_pids) - set(prev_firefox_pids))
    browser_pid = None
    if len(new_firefox_pids) == 1 :
        browser_pid = new_firefox_pids[0]
    return driver, browser_pid

def open_chrome(download_dir=None):
    chrome_profile = webdriver.ChromeOptions()
    if download_dir:        
        profile = {
               "download.default_directory":donwload_directory,
                "download.prompt_for_download": False,
               "download.directory_upgrade": True,
               "plugins.plugins_disabled": ["Chrome PDF Viewer"]}
        chrome_profile.add_experimental_option("prefs", profile)
        chrome_profile.add_argument("--disable-extensions")
    return webdriver.Chrome(chrome_options=chrome_profile)

def open_driver(download_dir=None):
    try:
        return open_chrome(download_dir)
    except:
        return open_firefox(download_dir)

def login(driver, params):
        print 'def login("%s"):' %(params['login-url'])
        driver.get(params['login-url'])
        time.sleep(3)
        handle_alert(driver)
        if 'username-control-name' in params:
            username_control = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, params['username-control-name'])))
        elif 'username-control-id' in params:
            username_control = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, params['username-control-id'])))
        else:
            raise Exception("please provide username-control-id or username-control-name")
        username_control.send_keys(params['username'])
        
        if 'password-control-name' in params:
            password_control = driver.find_element_by_name(params['password-control-name'])
        elif 'password-control-id' in params:
            password_control = driver.find_element_by_id(params['password-control-id'])
        else:
            raise Exception("please provide password-control-id or password-control-name")
        password_control.send_keys(params['password'])
        
        if 'submit-control-name' in params:
            element = driver.find_element_by_name(params['submit-control-name']).click()
        elif 'submit-control-id' in params:
            element = driver.find_element_by_id(params['submit-control-id']).click()
        else:
            password_control.submit()
            
        if 'sleep-time' in params:
            time.sleep(params['sleep-time'])
        else:
            time.sleep(3)
        handle_alert(driver)
        
        if 'confirm-control-id' in params:
            element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, params['confirm-control-id'])))
        elif 'confirm-control-name' in params:
            element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, params['confirm-control-name'])))
        else:
            time.sleep(10)
            
        print 'authendication done'
        print 'title:%s'%driver.title

def get_all_firefox_pids():
    process = subprocess.Popen('ps aux | grep "/usr/lib/firefox/firefox -foreground"',
                         shell=True,
                         stdout=subprocess.PIPE,
                       )
    stdout_list = process.communicate()[0].split('\n')
    current_username = getpass.getuser()
    firefox_pids = []
    for line in stdout_list:
        if line.startswith(current_username + ' ') and not "grep" in line :
            print line
            pid = int(line[len(current_username) + 1:].strip().split(' ')[0])
            firefox_pids.append(pid)
    return firefox_pids

def kill_browser(browser_pid):
    try:
        os.system("kill -9 %s" %(browser_pid))
        time.sleep(2)
    except:
        traceback.print_exc()

def handle_alert(driver):
    try:
        time.sleep(1)
        WebDriverWait(driver, 3).until(EC.alert_is_present())
        alert = driver.switch_to_alert()
        alert.accept()
        print "Alert was accepted"
    except UnexpectedAlertPresentException:
        alert.send_keys('8080')
        alert.dismiss()
    except:
        pass

def file_writerow(file_ptr, row):
    index = 0
    if type(row) == tuple:
        pass
    elif type(row) == list:
        pass
    elif type(row) == dict:
        row = dict.values()
    else:
        row = [row]

    for item in row:
       index += 1
       if isinstance(item, basestring):
           file_ptr.write('%s' %item.replace('\t', '    '))
       else:
           file_ptr.write('%s' %item)
       if index < len(row):
           file_ptr.write('\t')

    file_ptr.write('\n')

def is_html_document(file_path):
    f = codecs.open(file_path, 'r', 'utf-8')
    try:
        content = f.read()
        if content.find('<html') > 0 :
            return True
    except:
        print 'could not read the file as text. so not a html'
    f.close()


    return False


def download_file(url, file_path, cookies=None):
    if os.path.exists(file_path) :
        return 2
    print  'downloading "%s"' %(url)
    if url.startswith('http://www.tsa.gov/') or url.startswith('https://www.tsa.gov/') or \
        url.startswith('http://www.fema.gov/') or url.startswith('https://www.fema.gov/') or \
        url.startswith('http://www.cbp.gov/') or url.startswith('https://www.cbp.gov/') or \
        url.startswith('http://www.ice.gov/') or url.startswith('https://www.ice.gov/'):
        return 0
    try:
        if not cookies:
            cookies = []
        cp = urllib2.HTTPCookieProcessor()
        cj = cp.cookiejar
        for s_cookie in cookies:
            cj.set_cookie(
                cookielib.Cookie(
                    version=0
                    , name=s_cookie['name']
                    , value=s_cookie['value']
                    , port='80'
                    , port_specified=False
                    , domain=s_cookie['domain']
                    , domain_specified=True
                    , domain_initial_dot=False
                    , path=s_cookie['path']
                    , path_specified=True
                    , secure=s_cookie['secure']
                    , expires=None
                    , discard=False
                    , comment=None
                    , comment_url=None
                    , rest=None
                    , rfc2109=False
                )
            )
        opener = urllib2.build_opener(cp)
        response = opener.open(url)
    except:
        print traceback.print_exc()
        time.sleep(5)
        return 0
    print 'resposne code: %s' %(response.code)
    if response.code == 200:
        image_bytes = response.read()
        f = open(file_path, 'wb')
        f.write(image_bytes)
        f.close()
        time.sleep(1)
        return 1
    return 0

def resize_png_image(original_image_path, maxheight=None):
    image_dot_png_path = original_image_path
    if original_image_path[-4:] == '_png':
        image_dot_png_path = original_image_path[:-4] + ".png"
        shutil.copyfile(original_image_path, image_dot_png_path)

    base_image = Image.open(image_dot_png_path)
    (original_width, original_height) = base_image.size
    
    if maxheight:
        print 'original_height:', original_height
        print 'maxheight:', maxheight
        if original_height > maxheight:
            print 'crop height: %s to %s ' %(original_height, maxheight)
            base_image = base_image.crop((0, 0, original_width,maxheight))
            base_image.save(image_dot_png_path)
            shutil.copyfile(image_dot_png_path, original_image_path)

    original_file_size = os.stat(image_dot_png_path).st_size
    print 'original_file_size:', original_file_size

    (original_width, original_height) = base_image.size
            
    if original_file_size < 25000 :
        return True
    else:
        image_dot_png_path2 = image_dot_png_path[:-4] + "2.png"
        modified_file_size = 25000
        ratio = 1.0
        while True:
            ratio = ratio * 0.8
            print 'ratio:', ratio
            modified_width = int(round(original_width * ratio))
            modified_height = int(round(original_height * ratio))
            thumbnail_image = base_image.resize((modified_width, modified_height), Image.ANTIALIAS)
            thumbnail_image.save(image_dot_png_path2)
            del thumbnail_image
            modified_file_size = os.stat(image_dot_png_path2).st_size
            print modified_file_size
            if modified_file_size < 25000:
                shutil.move(image_dot_png_path2, original_image_path)
                return True

"""def jpeg_to_png(image_local_path):
    temp_jpeg_image_path = './thumbnails/temp.jpg'
    temp_png_image_path =  './thumbnails/temp.png'
    shutil.move(image_local_path, temp_jpeg_image_path)
    base_image = Image.open(temp_jpeg_image_path)
    base_image.save(temp_png_image_path)
    os.remove(temp_jpeg_image_path)
    shutil.move(temp_png_image_path, image_local_path)"""

def jpeg_to_png(jpg_file,png_file):#image_local_path):
    temp_jpeg_image_path = jpg_file
    temp_png_image_path =  png_file
    #shutil.move(image_local_path, temp_jpeg_image_path)
    base_image = Image.open(temp_jpeg_image_path)
    base_image.save(temp_png_image_path)
    os.remove(temp_jpeg_image_path)
    #shutil.move(temp_png_image_path, image_local_path)
    
def csv_writerow(file_ptr, row):
    index = 0
    for item in row:
       index += 1
       if isinstance(item, basestring) and (',' in item or '\t' in item or '\n' in item or '\r' in item or '"' in item):
           file_ptr.write('"')
           file_ptr.write('%s' %item.replace('"', '""'))
           file_ptr.write('"')
       else:
           file_ptr.write('%s' %item)
       if index < len(row):
           file_ptr.write(',')
           
    file_ptr.write('\n')
