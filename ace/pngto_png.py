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
import argparse
from PIL import Image
import urllib, cStringIO
import csv
import crawlutils
from optparse import OptionParser
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import glob

def main():
    folder="./downloads/"
    files=glob.glob1(folder, "*.png")
    for file1 in files:
       crawlutils.resize_png_image(folder+file1)
       shutil.copyfile(folder+file1, "./thumbnails_png/"+file1.replace(".png","_png"))
       


if __name__ == '__main__':
    main()
    
