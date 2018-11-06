#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import csv
import argparse


def main():
    doc_id=[]
    tid=[]
    page=[]
    last=[]
    lf=[]
    toc_tuple=[]

    with open('op1.csv', 'rb') as csvfile:
        smreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for i,row in enumerate(smreader):
            if i == 2140:
                break
            toc_tuple.append((row[0],row[2],row[3],row[4]))
            doc_id.append(row[0])
            tid.append(row[2])
            page.append(row[3])
            last.append(row[4])
            lf.append(row[5])

    j=0
    no_page=tid[-1]
    for (doc,toc,f,l) in toc_tuple:
        if f == 'NULL':
            continue

        doc_pdf=doc+".pdf"
        if no_page != toc:
            if doc_id[j] == doc_id[j+1]:
                    l=int(page[j+1])-1
                    print "l1:",l
            if lf[j+1]!='NULL':
                l=lf[j+1]
                print "l2:",l
        f=int(f)
        l=int(l)
        print "first page %d - last page %d" % (f, l)
        print "document_pdf %s"%doc_pdf
        print "toc_pdf %s.pdf"%toc
        if f==1:
            pdf="pdfseparate -f %d -l %d /home/vulcantech/kendavar/Ace/opentextbook/new/%s /home/vulcantech/kendavar/Ace/opentextbook/toc/%s.pdf"%(f,l,doc_pdf,toc)
        else:
            pdf="pdftk /home/vulcantech/kendavar/Ace/opentextbook/new/%s cat %d-%d output /home/vulcantech/kendavar/Ace/opentextbook/toc/%s.pdf"%(doc_pdf,f,l,toc)
        os.system(pdf)
  
        st="""echo 'update table_of_content set toc_pdf="/mnt/data/kendavar/opentextbooks/toc/%s.pdf" where id=%s;' | mysql -uaceuser -paceuser opentextbooks"""%(toc,toc)  
        file("opentext.sh","a").write(st+"\n")
        j+=1
    print "pdf created for chapters"
        


if __name__ and "__main__":
    main()

'''def main(args):
    list_id = args.id
    list_page = args.page
    correction = args.corr
    doc_pdf = args.doc_pdf
    no_page=list_page[-1]
    last=args.last
    reader = csv.reader(f)


    print "list_id length",len(list_id)
    i = 0
    for page in list_page:
        toc= list_id[i]
        i+= 1
        toc=str(toc)
        f= page + correction
        if page == no_page:
            l=last
        else:
            l= list_page[i] + correction-1
        print "first page %d - last page %d" % (f, l)
        print "document_pdf %s"%doc_pdf
        print "toc_pdf %s.pdf"%toc
        os.system("pdftk /home/vulcantech/kendavar/Ace/opentextbook/new/%s cat %d-%d output /home/vulcantech/kendavar/Ace/opentextbook/toc/%s.pdf"%(doc_pdf,f,l,toc))
  
        st="""echo 'update table_of_content set toc_pdf="/mnt/data/kendavar/opentextbooks/toc/%s.pdf" where id=%s;' | mysql -uaceuser -paceuser opentextbooks"""%(toc,toc)  
        file("opentext.sh","a").write(st+"\n")
    print "pdf created for chapters"

if __name__ and "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--i', dest='id',nargs='+',type=int, help='Give the id')
    parser.add_argument('--p', dest='page',nargs='+',type=int, help='Give the page')
    parser.add_argument('--doc', dest='doc_pdf',type=str, help='Give the document pdf')
    parser.add_argument('--l', dest='last',type=int,default=0, help='Give the correct value')
    parser.add_argument('--c', dest='corr',type=int,default=0, help='Give the correct value')

    args = parser.parse_args()

    main(args)'''
