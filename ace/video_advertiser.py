#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import re
from selenium import webdriver
import time
import os
import traceback
import requests
import urllib
import util
import optparse
import mx
import urllib2
import datetime
import codecs
from bs4 import BeautifulSoup as bs
from random import randint


def get_corr():
    s = ''
    for i in range(16):
        s = s + str(randint(0,9))
    return s


def get_url(anchor,video_links):
    for a in anchor:
        link=a["href"]
        if "/video/" in link:
            if link not in video_links:
                video_links.append("http://www.usatoday.com%s"%link)
    return video_links






def get_viral(url,driver):            
    link=None
    player=driver.find_element_by_class_name("featured-media-player-video")
    iframe=player.find_element_by_tag_name("iframe")
    iframe.click()
    time.sleep(30)
    driver.switch_to_frame(iframe)
    video=driver.find_elements_by_class_name("video-ads") 
    if video:
        a=video[0].find_elements_by_tag_name("a")
        if a:
            link1=a[0].get_attribute("href")
            res=requests.get(link1)
            link=res.url
    driver.switch_to_default_content()
    return link     
      
def get_links(url,domainid,domain,driver):
    links=[]
    pages=0
    urls=[]
    url_page=None
    if domainid==1:
        pages=8
        url_page="http://www.rantnow.com/category/videos/page"
    if domainid==3:
        pages=20
        url_page="http://time.com/videos/page"
    for i in range(pages):
        i+=1
        urls.append("%s/%s/"%(url_page,i))
    if not pages:
        urls.append(url)
    for url in urls:
        print url
        res=urllib2.urlopen(url).read()
        soup=bs(res)
        for tag in soup.findAll('a'):
            if tag.get('href', None):
                href=tag['href']
                if domainid==1:
                    if href.startswith("/category/videos/"):
                        href="http://www.rantnow.com%s"%href
                    if '/videos/' not in href:
                        href=None
                elif domainid==2:
                    if "?video_id" in href and not href.startswith("http"):
                        href="http://www.rantchic.com%s"%href
                    if '/videos/' not in href:
                        href=None
                elif domainid==3:
                    if not (re.search(r'http://time.com/\d{7}/.*?/',href) or re.search(r'http://time.com/.*?/\d{7}/.*?/',href)):
                        href=None
                elif domainid==4:
                    if not ('videos/' in href and not href.endswith("videos/")):
                        href=None
                if href:
                    if href not in links and domain in href:
                        links.append(href)


    video_links=[]
    if domainid==7:
        res=requests.get(url)
        soup=bs(res.text)
        ul=soup.find("ul",{"class":"grid media-grid-ul"})
        anchor=soup.findAll("a")


        latest_links=[]

        for a in anchor:
            link=a["href"]
            if "/latest/" in link:
                if link not in latest_links:
                    latest_links.append("http://www.usatoday.com%s"%link)
        for i,link in enumerate(latest_links):
            res=requests.get(link)
            soup=bs(res.text)
            ul=soup.find("ul",{"class":"grid media-grid-ul"})
            anchor=soup.findAll("a")
            video_links=get_url(anchor,video_links)
            if i == 20:
                break
            #if len(video_links)>250:
            #    break

    if domainid==5:
        res=requests.get(url)
        soup=bs(res.text)
        pg=soup.find("div",{"class":"pg-no-rail pg-wrapper "})
        a=pg.findAll("a")
        for link in a:
            try:
                href=link["href"]
                if href not in video_links:
                    if "/videos" in href:
                        href="http://edition.cnn.com%s"%href
                        video_links.append(href)
            except:
                pass


    if domainid==6:
        driver.get(url)
        main_column=driver.find_element_by_id("main-column")
        for i in range(5):
            driver.find_element_by_class_name("load-more").click()
            time.sleep(2)
        main_column=driver.find_element_by_id("main-column")
        links=main_column.find_elements_by_tag_name("a")
        for link in links:
            href=link.get_attribute("href")
            if '/video' in href:
                if href not in video_links:
                    if re.search(r'./\d{15}/.*?',href):
                        video_links.append(href)

    for link in video_links:
        if link not in links:
            #if len(links) > 250:
            links.append(link)
    return links

def video_crawl(driver,domainid,urlid,url,domain,inttime,table,total_links):
    links=get_links(url,domainid,domain,driver)
    print "%s has links :%s"%(domain,len(links))
    total_links=total_links+len(links)
    print total_links
    for srclink in links:
        try:
            driver.get(srclink)
            
            embed=""
            print "Source link :",srclink
            if 'rantnow.com' in url:
                embed="//div[@class='video-player-content']"
                time.sleep(5)
            elif 'rantchic.com' in url:
              
                embed =  "//div[@class='featured-media-player-video']"
                time.sleep(5)
            elif 'time.com' in url:
                embed="//figure[@class='primary-video-wrapper video-brightcove']" 
                time.sleep(5)
            elif 'http://edition.cnn.com' in url:
                time.sleep(5)
                embed="//div[@class='media__video--thumbnail-wrapper']"
            elif 'http://www.nytimes.com/' in url:
                time.sleep(2)
                embed="//div[@id='video-container']"
            elif 'http://www.usatoday.com/' in url:
                embed="//div[@class='ui-video  video-player-loaded']"  
                time.sleep(5)               
            if 'digitaltrends' not in url:
                #if url:
                try:
                      if srclink.endswith("viral-partners"):
                          link=get_viral(url,driver)
                          if link:
                              util.insert(domainid, urlid, link, srclink,inttime, table)
                      else:
                          video = driver.find_element_by_xpath(embed)
                          video.click()
                          time.sleep(3)
                          if 'rantchic.com' in url:
                              video.click()
                              time.sleep(1)
                      if len(driver.window_handles)>1:
                           driver.switch_to_window(driver.window_handles[1])
                      
                           print "Advt Url: %s"%driver.current_url
                           link=driver.current_url
                           print "######################\n"
                           driver.close()
                           driver.switch_to_window(driver.window_handles[0])
                           util.insert(domainid, urlid, link, srclink,inttime, table)
                except:
                    traceback.print_exc()
                    pass  
            else:
                res = urllib2.urlopen(srclink).read()
                data = res[res.find(', tag: "')+8:]
                url = data[:data.find('"')]
                vid = data[data.find("{content_id: '")+15:]
                vid = vid[:vid.find("'")]
                tmp=urllib.quote_plus(srclink)
                corr=get_corr()

                #url=url.replace("__random-number__",corr).replace("__item-mediaid__",vid).replace("__page-url__",tmp)
                url=url.replace("&correlator=__random-number__","").replace("__item-mediaid__",vid).replace("__page-url__",tmp)
                print url
                print "\n====================\n"
                tmp1=urllib2.urlopen(url).read()
                if "<AdTitle>" in tmp1:
                    #f=codecs.open("digital%s.html"%corr,"w","utf8")
                    #f.write(tmp1)
                    #f.close()
                    ad=tmp1[tmp1.find("&adurl=")+7:]
                    ad=ad[:ad.find("]]>")]
                    print "2.Advt: %s"%ad[:250]
                    link=ad[:250]
                    link=urllib.unquote_plus(link)
                    #res=requests.get(link)
                    #link=res.url
                    driver.get(link)
                    time.sleep(1)
                    link=driver.current_url
                    #link=urllib.unquote_plus(link)
                    util.insert(domainid, urlid, link, srclink,inttime, table)
        except:
            traceback.print_exc()
            pass
    return total_links

def main():   
    table="video_advertiser"
    domain_table="domain_master"
    url_table="url_master"
    total_links=0
    total_urls=0 
    display = None
    driver=None
    cursor = None
    #main code starts      
    starttime = 'Start Time : %s'%(mx.DateTime.now())
    print starttime

    s1time= mx.DateTime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
       
       from pyvirtualdisplay import Display
       display = Display(visible=0, size=(1000,900))
       display.start()
    except:
       print 'No Xvfb!'
    driver=webdriver.Chrome()
    inttime=int(mx.DateTime.now())  
    stime = 'Start Time : %s'%(mx.DateTime.now())
    sql = """SELECT a.urlid,a.domainid,a.url,b.domain FROM %s as a join %s as b 
    using (domainid)"""%(url_table,domain_table)
    if not cursor:
        cursor=util.cursor_define()
    cursor.execute (sql)
    urls = cursor.fetchall()
    total_urls += len(urls)
    num_urls_processed = "Total number of urls to be processed %s"%len(urls)
    print num_urls_processed
    for (domainid,urlid,url_link,domain,) in urls:
        total_links=video_crawl(driver,domainid,urlid,url_link,domain,inttime,table,total_links)

    
    print "Fetching Completed"
    endtime = 'End Time : %s'%(mx.DateTime.now())
    e1time=mx.DateTime.now().strftime("%Y-%m-%d %H:%M:%S")
    d1 = datetime.datetime.strptime(s1time, '%Y-%m-%d %H:%M:%S')
    d2 = datetime.datetime.strptime(e1time, '%Y-%m-%d %H:%M:%S')
    ttime= "Total time to crawl:%s"%str(d2-d1)
    print endtime  
    total_num_urls_processed = "Total number of links processed %s"%total_links
    #set filename for csv
    filename='./csv_folder/video_advertiser_%s.csv'%(str(mx.DateTime.now().strftime("%Y_%m_%d_%H_%M_%S")))
    sql="""select a.domain as src_domain,c.advertiser as advertiser_domain,count(c.advertiser) 
    as advertiser_per_domain from domain_master a,url_master b,%s c where a.domainid=b.domainid 
    and b.domainid=c.domainid and c.datetime_run=%s and c.advertiser is not null group by a.domain,
    c.advertiser"""%(table,inttime)

    util.create_csvfile(sql,filename,cursor)
    util.send_mail("Video Advertisers", total_num_urls_processed, starttime, endtime,ttime,filename)

    try:
        if cursor:
            cursor.close()
    except:
        pass

    # Browser close.
    if driver:
        driver.quit()
    if display:
        display.stop()

    try:
        cmd = """ps -ef | grep -v grep | grep 'screen 0 %sx%sx24' | awk '{print $2}' | 
        xargs kill -9"""%(1000,900)
        os.system(cmd)
    except:
       traceback.print_exc()


if __name__=='__main__':
    main()
