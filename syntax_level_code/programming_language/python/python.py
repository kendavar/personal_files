#declare private variable in class
class dog:
   __name="" #private variable are accessable onlly inside the class 

#.format let you put the string The brackets and characters within them 
#(called format fields) are replaced with the objects passed into the str.format() method.
# A number in the brackets refers to the position of the object passed into the str.format() method.
"{0} hello".format("yeah,")
>>> print 'The value of PI is approximately {0:.3f}.'.format(math.pi)
The value of PI is approximately 3.142.
'!s' (apply str()) and '!r' (apply repr()) can be used to convert the value before it is formatted.
>>> print 'The story of {0}, {1}, and {other}.'.format('Bill', 'Manfred',
...                                                    other='Georg')
The story of Bill, Manfred, and Georg.
>>> import math
>>> print 'The value of PI is approximately {}.'.format(math.pi)
The value of PI is approximately 3.14159265359.
>>> print 'The value of PI is approximately {!r}.'.format(math.pi)
The value of PI is approximately 3.141592653589793.


#ide for python
pychram

#debugging tool 
ipython


#used to get data from csv rows as list
with open('dwr12.csv','rb') as csvfile:
        reader=csv.reader(csvfile,delimiter='   ',quotechar='|')#reader is used to read csv
        for row in reader:
           print row#gives first row list
           print row[0]#gives the first column

#used to retrive a image from a url
file = cStringIO.StringIO(urllib.urlopen(url).read())
img = Image.open(file)
img.save(filename)#filename is the file path used


#unicode problem
u.encode('ascii', 'xmlcharrefreplace')#encode to xml format
https://docs.python.org/2/howto/unicode.html

#md5 creating doc_id
    import haslib
    m= hashlib.md5()
    m.update(title+url)#the title and the url from the keywords is used to create doc_id
    document_id = m.hexdigest()

#using ffmpeg i get the frame of the vidieo snap shot and save it as a png file.input file is a link mp4 
-i input vidio or audio file, -ss is time, -vframe is the numer of frame, outputfile
os.system("""ffmpeg -i %s -ss 00:00:00.435 -vframes 1 
  /home/vulcantech/kendavar/Ace/vi_screenshot/%s.png"""%(tmp,number))
 #using os.system we run it in linux terminal

#to get time from years ago
from datetime import datetime
from dateutil.relativedelta import relativedelta
three_yrs_ago = datetime.now() - relativedelta(years=3)
date=int(three_yrs_ago)


#import re
r-tells the search pattern
?-one or more instance
re.split(r"")


#from mysql to csv file
import csv
import MySQLdb
def create_csvfile(table,inttime,filename,cursor):
   sql="""select a.domain as src_domain,c.widget as widget,c.advertiser as 
   advertiser_domain,count(c.advertiser) as advertiser_per_domain from domain_master a,feed_master b,
   %s c where a.domainid=b.domainid and b.domainid=c.domainid and c.datetime_run=%s group by a.domain,
   c.advertiser"""
   cursor.execute(sql,(table,inttime,filename))
   result=cursor.fetchall()
   fd=open("temp.csv","wb")
   writer = csv.DictWriter(fd, fieldnames = ["src_domain","widget","advertiser_domain","advertiser_per_domain"]
])
   writer.writeheader()
   c = csv.writer(fd)
   for row in result:
      c.writerow(row)
   fd.close()


#python unqute
import urllib

The + does the decoding of url +url
and other does the decoding to normal url
quote is done to make the url more parameter free

urlib.unqute_plus("%3a%2f%2fclickserv.sitescout.c")
urlib.unquote(%3a%2f%2fclickserv.sitescout.c)

#different between str and repr
str - any format to human understandable string
repr - any format to code which is for interperter
str("hello")
hello
repr("hello")
"'hello'"

#print the string in different forms
str.rjust()- right justifiy a string
str.ljust() -left justifiy a string 
str.zfill() - pad zeros on left
>>> '12'.zfill(5)
'00012'
>>> '-3.14'.zfill(7)
'-003.14'
>>> '3.14159265359'.zfill(5)
'3.14159265359'


#python how to select first two values in list in python


from itertools import izip

def pairwise(iterable):
    "s -> (s0,s1), (s2,s3), (s4, s5), ..."
    a = iter(iterable)
    return izip(a, a)

   for x, y in pairwise(list_page):
        print "%d + %d = %d" % (x, y, x + y)


#pass a list in arg parser
parser.add_argument('--p', dest='page',nargs='+',type=int, help='Give the page')

#convert xml to dict
#*********************************************************************************
#!/usr/bin/python

import requests
import xmltodict
import json
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

if len(sys.argv)>1:
    url=sys.argv[1].strip()
    res=requests.get(url)
    data = json.loads(json.dumps((xmltodict.parse(res.text))))
    print data.keys()
    print len(data['searchResponse']['SearchResults']['records']['rec'])
    for row in data['searchResponse']['SearchResults']['records']['rec']:
        print row
        print
#********************************************************************************
