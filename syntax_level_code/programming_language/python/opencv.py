#image processing
sudo pip install matplotlib
sudo apt-get install libopencv-dev python-opencv
sudo apt-get install python-tk

import cv2
import numpy as np
import matplotlib.pyplot as plt

#image is converted to gray to make processing easy
#cv2.IMREAD_GRAYSCALE - 0
#cv2.IMREAD_COLOR - 1
#cv2.IMREAD_UNCHANGED - -1
#eg:- img=cv2.imread('15.png',cv2.IMREAD_GRAYSCALE)
img=cv2.imread('15.png',0)
plt.imshow(img,cmap='gray',interpolation='bicubic')

#set a line in image
plt.plot([50,100],[80,100],'c',linewidth=5)
plt.show()

#save the image
cv2.imwrite('watch.png',img)
